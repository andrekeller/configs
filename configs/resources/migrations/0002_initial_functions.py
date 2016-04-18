"""
confi.gs resources server-side functions migrations
"""
from django.db import migrations


class Migration(migrations.Migration):
    """
    confi.gs resources server-side functions initial migration
    """
    dependencies = [
        ('resources', '0001_initial_schema'),
    ]

    operations = [
        migrations.RunSQL('''
          CREATE OR REPLACE FUNCTION find_free_block (
            arg_vrf INTEGER,
            arg_parent CIDR,
            arg_len INTEGER
          ) RETURNS CIDR AS $$
            DECLARE
              parent_family INTEGER;
              current_block CIDR;
              max_len INTEGER;
              covering CIDR;
            BEGIN
              covering := NULL;

              -- cannot assign a block larger than its parent
              IF masklen(arg_parent) > arg_len THEN
                RAISE EXCEPTION 'Requested prefixlen smaller than parents';
              END IF;

              -- determine max prefixlen, based on parents address family
              parent_family := family(arg_parent);
              IF parent_family = 4 THEN
                max_len := 32;
              ELSE
                max_len := 128;
              END IF;

              -- cannot assign a block shorter than address family supports.
              IF arg_len > max_len THEN
                RAISE EXCEPTION 'Requested prefixlen exceeds max prefixlen';
              END IF;

              -- cannot assign a block if parent is a host address (/32, /128)
              IF masklen(arg_parent) = max_len THEN
                RAISE EXCEPTION 'Parent block is a host address';
              END IF;

              -- loop until a free block is found or the returned block would
              -- no longer fit into the parent block.
              SELECT set_masklen(arg_parent, arg_len) INTO current_block;
              WHILE set_masklen(current_block, masklen(arg_parent)) <=
                    broadcast(arg_parent) LOOP

                -- exact match found, continue with next block
                IF EXISTS (SELECT 1 FROM resources_network
                             WHERE vrf_id = arg_vrf
                               AND network = current_block
                          ) THEN
                  SELECT broadcast(current_block) + 1 INTO current_block;
                  CONTINUE;
                END IF;

                -- covering match found, continue with block adjacent to
                -- covering match
                covering := (SELECT network FROM resources_network
                               WHERE vrf_id = arg_vrf
                                 AND network >>= current_block
                                 AND network << arg_parent
                               ORDER BY masklen(network) ASC LIMIT 1
                            );
                IF covering IS NOT NULL THEN
                  SELECT set_masklen(broadcast(covering) + 1,
                                     arg_len)
                  INTO current_block;
                  CONTINUE;
                END IF;

                -- new block would not be empty, continue with next block
                IF EXISTS (SELECT 1 FROM resources_network
                                      WHERE vrf_id = arg_vrf
                                        AND network <<= current_block
                          ) THEN
                  SELECT broadcast(current_block) + 1 INTO current_block;
                  CONTINUE;
                END IF;

                IF ((parent_family = 4 AND masklen(arg_parent) < 31) OR
                    parent_family = 6 AND masklen(arg_parent) < 127) THEN
                  IF (set_masklen(network(arg_parent),
                                  max_len) = current_block) THEN
                    SELECT broadcast(current_block) + 1 INTO current_block;
                    CONTINUE;
                  END IF;
                  IF (set_masklen(broadcast(arg_parent),
                                  max_len) = current_block) THEN
                    SELECT broadcast(current_block) + 1 INTO current_block;
                    CONTINUE;
                  END IF;
                END IF;

                -- we found a usable block, yay!
                RETURN current_block;

              END LOOP;

              RETURN NULL;
            END;
          $$ LANGUAGE plpgsql;
        '''),
        migrations.RunSQL('''
          CREATE OR REPLACE FUNCTION find_largest_free_block(
            arg_vrf INTEGER,
            arg_parent CIDR
          ) RETURNS CIDR AS $$
            DECLARE
              max_len INTEGER;
              parent_family INTEGER;
              free_block CIDR;
            BEGIN
              -- determine max prefixlen, based on parents address family
              parent_family := family(arg_parent);
              IF parent_family = 4 THEN
                max_len := 32;
              ELSE
                max_len := 128;
              END IF;
              FOR prefixlen IN masklen(arg_parent) .. max_len LOOP
                free_block = find_free_block(arg_vrf, arg_parent, prefixlen);
                IF free_block IS NOT NULL THEN
                  RETURN free_block;
                END IF;
              END LOOP;
              RETURN NULL;
            END;
          $$ LANGUAGE plpgsql;
        ''')
    ]

import csv


def write_hosts(filename, infoblox, infoblox_dns, zonefile, recordfile):
    print("writing hosts")

    with open(filename, 'r') as steamfile:
        reader = csv.reader(steamfile)
        zone_writer = csv.writer(open(zonefile, 'w'), delimiter=';')
        zone_writer.writerow(["header-authzone;fqdn*;zone_format*;allow_active_dir;allow_query;allow_transfer"
                              ";allow_update;allow_update_forwarding;comment;create_underscore_zones"
                              ";ddns_force_creation_timestamp_update;ddns_principal_group;ddns_principal_tracking"
                              ";ddns_restrict_patterns;ddns_restrict_patterns_list;ddns_restrict_protected"
                              ";ddns_restrict_secure;ddns_restrict_static;disable_forwarding;disabled"
                              ";enable_fixed_rrset_order;external_primaries;external_secondaries;grid_primaries"
                              ";grid_secondaries;is_multimaster;notify_delay;ns_group;prefix;_new_prefix"
                              ";soa_default_ttl;soa_email;soa_expire;soa_mnames;soa_negative_ttl;soa_refresh"
                              ";soa_retry;soa_serial_number;update_forwarding;view;zone_type"])
        record_writer = csv.writer(open(recordfile, 'w'), delimiter=';')
        record_writer.writerow(["header-arecord;address*;_new_address;fqdn*;_new_fqdn;comment;create_ptr;creator"
                                ";ddns_principal;ddns_protected;disabled;ttl;view"])

        for row in reader:
            if str('*') in row[0]:
                stripfqdn = (row[0].replace("*.", ""))
                formatstr = "authzone;{fqdn};FORWARD;;;;;;;FALSE;;;;;;;;;FALSE;FALSE;FALSE;;;{" \
                            "infoblox_dns}/False/False/False;;FALSE;;;;;;;;;;;;2;;default;Authoritative"
                infobloxstr = formatstr.format(fqdn=stripfqdn, infoblox_dns=infoblox_dns)
                zone_writer.writerow([infobloxstr])
                print(infobloxstr)
            else:
                if not str('*') in row[0]:
                    formatstr = "authzone;{fqdn};FORWARD;;;;;;;FALSE;;;;;;;;;FALSE;FALSE;FALSE;;;{" \
                                "infoblox_dns}/False/False/False;;FALSE;;;;;;;;;;;;2;;default;Authoritative"
                    infobloxstr = formatstr.format(fqdn=row[0], infoblox_dns=infoblox_dns)
                    zone_writer.writerow([infobloxstr])
                    print(infobloxstr)

            formatstr = "arecord;{infoblox_addr};;{fqdn};;;FALSE;STATIC;;FALSE;FALSE;;default"
            infobloxstr = formatstr.format(infoblox_addr=infoblox, fqdn=row[0])
            record_writer.writerow([infobloxstr])
            print(infobloxstr)


write_hosts('steam.txt', '172.16.254.10', 'ns01.event.networked.pro', 'zones.csv', 'records.csv')

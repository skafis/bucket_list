drop table if exists bucket_list;
create table bucket_list(
    id integer primary key autoincrement,
    bucketlist_name text not null,
    bucketlist_description text
);


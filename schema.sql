drop table if exists redirects;
drop table if exists reports;

-- Active redirects
create table redirects(
	id integer primary key autoincrement -- could probably get away with uid as p.k.
	, lid text key -- when we migrate to pgsql varchar(8)
	, url text key -- when we migrate to pgsql some other varchar
	, ip not null  -- the IP address of the user who created the URL
	, created timestamp not null default current_timestamp
	,
);

-- Table where people can report bad links by ID
create table reports(
	id integer primary key autoincrement
	, url text not null
	, ip text not null
	, reporter_ip text not null
	, created timestamp not null
	, reported timestamp not null default current_timestamp
);


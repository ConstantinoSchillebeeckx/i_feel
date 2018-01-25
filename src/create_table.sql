DROP TABLE IF EXISTS raw_query;
CREATE TABLE public.raw_query (
    "pk" SERIAL,
	"approved_at_utc" varchar NULL,
	"approved_by" varchar NULL,
	"archived" bool NULL,
	"author" varchar NULL,
	"author_cakeday" varchar NULL,
	"author_flair_css_class" varchar NULL,
	"author_flair_text" varchar NULL,
	"banned_at_utc" varchar NULL,
	"banned_by" varchar NULL,
	"brand_safe" bool NULL,
	"can_gild" bool NULL,
	"can_mod_post" bool NULL,
	"clicked" bool NULL,
	"comment_limit" varchar NULL,
	"comment_sort" varchar NULL,
    "contest_mode" varchar NULL,
    "created" float NULL,
    "created_utc" float NULL,
    "crosspost_parent" varchar NULL,
    "distinguished" varchar NULL,
    "domain" varchar NULL,
    "downs" varchar NULL,
    "downloaded_utc" varchar NULL,
    "edited" varchar NULL,
    "gilded" varchar NULL,
    "hidden" varchar NULL,
    "hide_score" varchar NULL,
    "id" varchar NULL,
    "is_crosspostable" bool NULL,
    "is_reddit_media_domain" bool NULL,
    "is_self" bool NULL,
    "is_video" bool NULL,
    "likes" varchar NULL,
    "link_flair_css_class" varchar NULL,
    "link_flair_text" varchar NULL,
    "locked" bool NULL,
    "media" varchar NULL,
    "mod_note" varchar NULL,
    "mod_reason_by" varchar NULL,
    "mod_reason_title" varchar NULL,
    "name" varchar NULL,
    "num_comments" varchar NULL,
    "num_crossposts" varchar NULL,
    "num_reports" varchar NULL,
    "over_18" bool NULL,
	"parent_whitelist_status" varchar NULL,
    "permalink" varchar NULL,
    "pinned" bool NULL,
    "post_hint" varchar NULL,
    "quarantine" varchar NULL,
    "removal_reason" varchar NULL,
    "report_reasons" varchar NULL,
    "saved" bool NULL,
    "score" varchar NULL,
    "secure_media" varchar NULL,
    "selftext" varchar NULL,
    "selftext_html" varchar NULL,
	"spoiler" bool NULL,
    "stickied" bool NULL,
    "subreddit" varchar NULL,
    "subreddit_id" varchar NULL,
    "subreddit_name_prefixed" varchar NULL,
    "subreddit_type" varchar NULL,
    "suggested_sort" varchar NULL,
    "thumbnail" varchar NULL,
    "thumbnail_height" varchar NULL,
    "thumbnail_width" varchar NULL,
    "title" varchar NULL,
    "ups" varchar NULL,
	"url" varchar NULL,
    "view_count" varchar NULL,
    "visited" bool NULL,
    "whitelist_status" varchar NULL
)
WITH (
	OIDS=FALSE
) ;


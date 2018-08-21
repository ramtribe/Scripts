# Copyright 2014 Facebook, Inc.

# You are hereby granted a non-exclusive, worldwide, royalty-free license to
# use, copy, modify, and distribute this software in source code or binary
# form for use in connection with the web services and APIs provided by
# Facebook.

# As with any software that integrates with the Facebook platform, your use
# of this software is subject to the Facebook Developer Principles and
# Policies [http://developers.facebook.com/policy/]. This copyright notice
# shall be included in all copies or substantial portions of the software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.adsinsights import AdsInsights
from facebookads.api import FacebookAdsApi

access_token = 'EAAYKDY2cR9EBAGDS1MZBIcSff2Mb11q88KjOMFN27LCy8QpyvnmDqPbMgXF0zDcEpTfs5yQmsrTGX9wXGNbGOKWsSNmXgGsBD3OILq8LQlt7ZCIfyfZCKGZB3toSvvXb0qktmnRNt9cNQI8zmZB8YsnXNDwT0HSWmyeBEi8eriEIkZCoZA0kLL1MXY1kKoW5GRMW5YHPHgp7mvqQEyBPUCE'
ad_account_id = 'act_1532270523544349'
app_secret = '9d5909a2e9c23f3d923dcb2fc37257ff'
app_id = '1699903186946001'
FacebookAdsApi.init(access_token=access_token)

fields = [
    'results',
    'result_rate',
    'reach',
    'frequency',
    'impressions',
    'delivery',
    'relevance_score:score',
    'spend',
    'impressions_gross',
    'impressions_auto_refresh',
    'cost_per_result',
    'cpp',
    'cpm',
    'actions:page_engagement',
    'actions:like',
    'actions:comment',
    'actions:post_engagement',
    'actions:post_reaction',
    'actions:post',
    'actions:photo_view',
    'actions:rsvp',
    'actions:receive_offer',
    'actions:checkin',
    'cost_per_action_type:page_engagement',
    'cost_per_action_type:like',
    'cost_per_action_type:comment',
    'cost_per_action_type:post_engagement',
    'cost_per_action_type:post_reaction',
    'cost_per_action_type:post',
    'cost_per_action_type:photo_view',
    'cost_per_action_type:rsvp',
    'cost_per_action_type:receive_offer',
    'cost_per_action_type:checkin',
    'unique_video_continuous_2_sec_watched_actions:video_view',
    'video_continuous_2_sec_watched_actions:video_view',
    'actions:video_view',
    'video_10_sec_watched_actions:video_view',
    'video_30_sec_watched_actions:video_view',
    'video_p25_watched_actions:video_view',
    'video_p50_watched_actions:video_view',
    'video_p75_watched_actions:video_view',
    'video_p95_watched_actions:video_view',
    'video_p100_watched_actions:video_view',
    'video_avg_time_watched_actions:video_view',
    'video_avg_percent_watched_actions:video_view',
    'canvas_avg_view_time',
    'canvas_avg_view_percent',
    'cost_per_2_sec_continuous_video_view:video_view',
    'cost_per_action_type:video_view',
    'cost_per_10_sec_video_view:video_view',
    'actions:link_click',
    'unique_actions:link_click',
    'outbound_clicks:outbound_click',
    'unique_outbound_clicks:outbound_click',
    'website_ctr:link_click',
    'unique_link_clicks_ctr',
    'outbound_clicks_ctr:outbound_click',
    'unique_outbound_clicks_ctr:outbound_click',
    'clicks',
    'unique_clicks',
    'ctr',
    'unique_ctr',
    'cost_per_action_type:link_click',
    'cost_per_unique_action_type:link_click',
    'cost_per_outbound_click:outbound_click',
    'cost_per_unique_outbound_click:outbound_click',
    'cpc',
    'cost_per_unique_click',
    'estimated_ad_recallers',
    'estimated_ad_recall_rate',
    'cost_per_estimated_ad_recallers',
    'total_action_value',
    'actions:games_plays',
    'actions:app_engagement',
    'actions:app_install',
    'actions:app_story',
    'actions:app_use',
    'actions:credit_spent',
    'actions:app_custom_event_fb_mobile_achievement_unlocked',
    'actions:app_custom_event',
    'actions:app_custom_event_fb_mobile_add_to_cart',
    'actions:app_custom_event_fb_mobile_add_to_wishlist',
    'actions:app_custom_event_fb_mobile_initiated_checkout',
    'actions:app_custom_event_fb_mobile_content_view',
    'actions:app_custom_event_fb_mobile_spent_credits',
    'actions:mobile_app_install',
    'actions:app_custom_event_fb_mobile_level_achieved',
    'actions:app_custom_event_fb_mobile_add_payment_info',
    'actions:app_custom_event_fb_mobile_purchase',
    'actions:app_custom_event_fb_mobile_rate',
    'actions:app_custom_event_fb_mobile_complete_registration',
    'actions:app_custom_event_fb_mobile_search',
    'actions:app_custom_event_fb_mobile_activate_app',
    'actions:app_custom_event_fb_mobile_tutorial_completion',
    'actions:app_custom_event_other',
    'unique_actions:app_custom_event_fb_mobile_achievement_unlocked',
    'unique_actions:app_custom_event_fb_mobile_add_to_cart',
    'unique_actions:app_custom_event_fb_mobile_add_to_wishlist',
    'unique_actions:app_custom_event_fb_mobile_initiated_checkout',
    'unique_actions:app_custom_event_fb_mobile_content_view',
    'unique_actions:app_custom_event_fb_mobile_spent_credits',
    'unique_actions:app_custom_event_fb_mobile_level_achieved',
    'unique_actions:app_custom_event_fb_mobile_add_payment_info',
    'unique_actions:app_custom_event_fb_mobile_purchase',
    'unique_actions:app_custom_event_fb_mobile_rate',
    'unique_actions:app_custom_event_fb_mobile_complete_registration',
    'unique_actions:app_custom_event_fb_mobile_search',
    'unique_actions:app_custom_event_fb_mobile_activate_app',
    'unique_actions:app_custom_event_fb_mobile_tutorial_completion',
    'cost_per_action_type:games_plays',
    'cost_per_action_type:app_engagement',
    'cost_per_action_type:app_install',
    'cost_per_action_type:app_story',
    'cost_per_action_type:app_use',
    'cost_per_action_type:credit_spent',
    'cost_per_action_type:app_custom_event_fb_mobile_achievement_unlocked',
    'cost_per_action_type:app_custom_event',
    'cost_per_action_type:app_custom_event_fb_mobile_add_to_cart',
    'cost_per_action_type:app_custom_event_fb_mobile_add_to_wishlist',
    'cost_per_action_type:app_custom_event_fb_mobile_initiated_checkout',
    'cost_per_action_type:app_custom_event_fb_mobile_content_view',
    'cost_per_action_type:app_custom_event_fb_mobile_spent_credits',
    'cost_per_action_type:mobile_app_install',
    'cost_per_action_type:app_custom_event_fb_mobile_level_achieved',
    'cost_per_action_type:app_custom_event_fb_mobile_add_payment_info',
    'cost_per_action_type:app_custom_event_fb_mobile_purchase',
    'cost_per_action_type:app_custom_event_fb_mobile_rate',
    'cost_per_action_type:app_custom_event_fb_mobile_complete_registration',
    'cost_per_action_type:app_custom_event_fb_mobile_search',
    'cost_per_action_type:app_custom_event_fb_mobile_activate_app',
    'cost_per_action_type:app_custom_event_fb_mobile_tutorial_completion',
    'cost_per_action_type:app_custom_event_other',
    'cost_per_unique_action_type:app_custom_event_fb_mobile_achievement_unlocked',
    'cost_per_unique_action_type:app_custom_event_fb_mobile_add_to_cart',
    'cost_per_unique_action_type:app_custom_event_fb_mobile_add_to_wishlist',
    'cost_per_unique_action_type:app_custom_event_fb_mobile_initiated_checkout',
    'cost_per_unique_action_type:app_custom_event_fb_mobile_content_view',
    'cost_per_unique_action_type:app_custom_event_fb_mobile_spent_credits',
    'cost_per_unique_action_type:app_custom_event_fb_mobile_level_achieved',
    'cost_per_unique_action_type:app_custom_event_fb_mobile_add_payment_info',
    'cost_per_unique_action_type:app_custom_event_fb_mobile_purchase',
    'cost_per_unique_action_type:app_custom_event_fb_mobile_rate',
    'cost_per_unique_action_type:app_custom_event_fb_mobile_complete_registration',
    'cost_per_unique_action_type:app_custom_event_fb_mobile_search',
    'cost_per_unique_action_type:app_custom_event_fb_mobile_activate_app',
    'cost_per_unique_action_type:app_custom_event_fb_mobile_tutorial_completion',
    'mobile_app_purchase_roas:app_custom_event_fb_mobile_purchase',
    'action_values:app_custom_event_fb_mobile_content_view',
    'action_values:app_custom_event_fb_mobile_rate',
    'action_values:app_custom_event_fb_mobile_add_to_cart',
    'action_values:app_custom_event_fb_mobile_add_to_wishlist',
    'action_values:app_custom_event_fb_mobile_initiated_checkout',
    'action_values:app_custom_event_fb_mobile_purchase',
    'action_values:app_custom_event_fb_mobile_search',
    'action_values:app_custom_event_fb_mobile_spent_credits',
    'action_values:credit_spent',
    'actions:onsite_conversion_purchase',
    'actions:onsite_conversion_flow_complete',
    'actions:leadgen_other',
    'cost_per_action_type:onsite_conversion_purchase',
    'cost_per_action_type:onsite_conversion_flow_complete',
    'cost_per_action_type:leadgen_other',
    'action_values:onsite_conversion_purchase',
    'action_values:onsite_conversion_flow_complete',
    'date_start',
    'date_stop',
    'account_id',
    'account_name',
    'campaign_group_name',
    'campaign_group_id',
    'campaign_name',
    'campaign_id',
    'adgroup_id',
    'adgroup_name',
    'objective',
    'buying_type',
    'start_time',
    'stop_time',
    'bid',
    'budget',
    'schedule',
    'split_test_split',
    'split_test_variable',
    'optimization_results',
    'cost_per_optimization_result',
    'last_significant_edit',
]
params = {
    'level': 'account',
    'filtering': [],
    'breakdowns': ['days_1','country','ad_id'],
    'time_range': {'since':'2017-01-01','until':'2018-07-01'},
}
print AdAccount(ad_account_id).get_insights(
    fields=fields,
    params=params,
)


source 'https://rubygems.org'

gem 'jekyll'

# Transitive dependencies pinned to a minimum patched version for known CVEs.
# Remove the pin once the parent gem's own dependency floor catches up.
gem 'json', '>= 2.21.2'      # CVE-2026-71847: UAF in JSON::ResumableParser#partial_value
                             # (supersedes the >= 2.19.9 pin for CVE-2026-54696)
gem 'loofah', '>= 2.25.2'    # GHSA-9wjq-cp2p-hrgf, GHSA-5qhf-9phg-95m2, GHSA-8whx-365g-h9vv
gem 'nokogiri', '>= 1.19.4'  # latest security/hardening release in the 1.19.x line

# Core plugins that directly affect site building
group :jekyll_plugins do
    gem 'jekyll-archives-v2'
    gem 'jekyll-cache-bust'
    gem 'jekyll-email-protect'
    gem 'jekyll-feed'
    gem 'jekyll-get-json'
    gem 'jekyll-imagemagick'
    gem 'jekyll-jupyter-notebook'
    gem 'jekyll-link-attributes'
    gem 'jekyll-minifier'
    gem 'jekyll-paginate-v2'
	gem 'jekyll-regex-replace'
    gem 'jekyll-scholar'
    gem 'jekyll-sitemap'
    gem 'jekyll-socials'
    gem 'jekyll-tabs'
    gem 'jekyll-terser', :git => "https://github.com/RobertoJBeltran/jekyll-terser.git"
    gem 'jekyll-toc'
    gem 'jekyll-twitter-plugin'
    gem 'jemoji'

    gem 'classifier-reborn'  # used for content categorization during the build
end

# Gems for development or external data fetching (outside :jekyll_plugins)
group :other_plugins do
    # css_parser >= 3.0.0 fixes CVE-2026-53727 (SSRF / local file disclosure in
    # read_remote_file). The fix was not backported to 1.x or 2.x. The gem
    # jekyll-3rd-party-libraries was removed from :jekyll_plugins because its
    # `css_parser (< 2.0)` ceiling blocked this upgrade; the vendored
    # _plugins/download-3rd-party.rb provides the equivalent functionality.
    # Requires Ruby >= 3.2 (CI runs 3.3.5 / 3.2.2).
    gem 'css_parser', '>= 3.0.0'
    gem 'feedjira'
    gem 'httparty'
    gem 'observer'       # used by jekyll-scholar
    gem 'ostruct'        # used by jekyll-twitter-plugin
    # gem 'terser'         # used by jekyll-terser
    # gem 'unicode_utils' -- should be already installed by jekyll
    # gem 'webrick' -- should be already installed by jekyll
end

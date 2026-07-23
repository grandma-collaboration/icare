from playwright.sync_api import expect


def test_patch_icare(super_admin_user, page):
    page.goto(f"/become_user/{super_admin_user.id}")
    page.goto("/")
    expect(page.locator('//*[contains(.,"Icare")]').first).to_be_visible(timeout=20000)


def test_grandma_dashboard_recent_sources(super_admin_user, page):
    # The GRANDMA dashboard's RecentSources widget (and the DynamicTagDisplay it
    # renders) reads groups/profile/taxonomies/recentSources via RTK Query hooks.
    # If any still read a removed redux slice, the widget throws on render and
    # this heading never appears -- so it guards the RTK Query migration.
    page.goto(f"/become_user/{super_admin_user.id}")
    page.goto("/")
    expect(
        page.get_by_role("heading", name="Recent Sources").first
    ).to_be_visible(timeout=20000)

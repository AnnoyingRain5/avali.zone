# Avali.zone! The home of the avali.

This is the code repo for [avali.zone](https://avali.zone), the home of the Avali!

## Todo:

- Switch to dynamically generating main/templates/content and main/templates/groups
    - each content or group should include the following:
        - name
        - description
        - order (int)
        - links
            - this should be in a seperate table, so I can `SELECT * FROM links WHERE groupid = ?`
            - links have a name and destination
        - type
            - type should be a seperate table that has a name and order (int)
        - owner
    - Only admin can reorder or add content 
    - admin can also assign owners, who can manage name, description and links

- Content/group mini-sites (pages)
    - TLDR: allow group or content owners to control a sub-site
    - allow content editing, custom backgrounds (css?) and subpages of subpages

- Changing permissions on the website, not through scripts
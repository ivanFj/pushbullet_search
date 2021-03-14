ACCESS_TOKEN = {"Access-Token" : "o.tYINVKNMCABJX6Icag5ldJ2X6p7KyMog"}

##def load_pushes_file():
##
##    with open(PUSHES_FILE, "r") as pb_file:
##
##        pushes = json.load(pb_file)
##
##    return pushes['pushes']

##def compare_pushes_url(pushes, size, index, duplicate_urls):
##
##    ref_push = pushes[index]
##    ref_url = ref_push.get("url", False)
##
##    for j in range(index + 1, size):
##        other_push = pushes[j]
##        other_url = other_push.get("url", None)
##
##        if ref_url == other_url and other_push not in duplicate_urls:
##            duplicate_urls.append(other_push)

def get():

    ##all_pushes = load_pushes_file()

    size = len(all_pushes)
    page = int(self.request.get("page", 1))

    if page > 1:
        previous_page = u'href="?page={0}"'.format(int(page) - 1)
        disable_previous = ""
    else:
        previous_page = ""
        disable_previous = "disabled"

    push_range = 20
    upper_limit = page * push_range
    
    if upper_limit > size:
        upper_limit = size;
        next_page = ""
        disable_next = "disabled"
    else:
        next_page = u"href='?page={0}'".format(int(page) + 1)
        disable_next = ""
    
    lower_limit = upper_limit - push_range

    html_pushes = ""
    push_base = u"""<div class="mdl-cell mdl-cell--12-col mdl-color--white mdl-shadow--4dp pushes" data-iden='{iden}'>
                        <div class="loading hide">
                            <span class="loading-text"></span>
                            <div class="mdl-spinner mdl-js-spinner is-active"></div>
                        </div>
                        <div class='fade-div'></div>
                        {title}
                        {body}
                        {url}
                        <div class='mdl-card__actions'>
                            <button class="mdl-button mdl-js-button mdl-button--raised mdl-button--accent mdl-js-ripple-effect delete">
                                <i class="material-icons">delete</i><span class="icon-text"> Delete</span>
                            </button>
                            <button class="mdl-button mdl-js-button mdl-button--raised mdl-button--accent mdl-js-ripple-effect change">
                                <i class="material-icons">edit</i><span class="icon-text"> Edit</span>
                            </button>
                        </div>
                </div>"""
    
    for index in range(lower_limit, upper_limit):

        push = all_pushes[index]
        
        html_push_title = ''
        html_push_body = ''
        html_push_url = ''

        title = push.get("title", "")
        body = push.get("body", "")
        url = push.get("url", "")
        iden = push.get("iden")

        if title:
            html_push_title = u"<h5 class='title'>{0}</h5>".format(title)

        if body:
            html_push_body = u"<p class='body'>{0}</p>".format(body)

        if url :
            html_push_url = u"<a class='url' href='{0}'>{0}</a>".format(url)

        html_pushes += push_base.format(title = html_push_title, body = html_push_body, url = html_push_url, iden = iden)

    return {"pushes" : html_pushes, "previouspage" : previous_page, "nextpage" : next_page, "disableprevious" : disable_previous, "disablenext" : disable_next}
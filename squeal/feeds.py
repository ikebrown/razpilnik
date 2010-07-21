from django.contrib.syndication.views import Feed
from models import *

class LatestSqueals(Feed):
 title = "Razpilnik! Latest squeals"
 link = "/"
 description = "The latest noise in the Razpilnik!"

 def items(self):
  return Squeal.objects.order_by('-pub_date')[:20]

 def item_title(self, item):
     title = item.author.user.username + " said: "
     if len(item.content) > 64: title += item.content[:64] + "..."
     else: title += item.content
     return title

 def item_description(self, item):
  return item.content

 def item_link(self, item):
  return "/" + item.author.user.username + "/squeal/" + str(item.id)

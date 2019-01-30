from pyramid.view import view_config
from repoll.models.main_models import *
import transaction

""" 
    For each notification, there'll be at least 2 leads:
        
"""

def user_followings(request, user_id):
    user = request.dbsession.query(User).filter(User.id==user_id).first()
    followings = user.following
    followings = [user.id for user in followings]
    return followings


@view_config(route_name='notifications_page', renderer='../templates/notifications_mobile.jinja2')
def notifications_page(request):
    if request.user:
        user = request.dbsession.query(User).filter(User.id==request.user.id).first()
        return {'user': user, 'user_id': user.id}
    return {}

@view_config(route_name='get_notifications', renderer='json')
def get_unseen_notifications(request):
    user_id = request.matchdict.get('user_id')
    notification_ids = []
    new_object_id = None
    unseen_notifications = []

    if not request.user: 
        request.response.status = '404'
        return {}
    elif request.user.id != int(user_id):
        request.response.status = '404'
        return {}
        
    dictt = {}
    notifications = request.dbsession.query(Notification).filter(Notification.user_id==user_id)
    notifications = notifications[::-1]
    for notif in notifications:
        notification_ids.append(notif.id)
        n_object_id = notif.object_id
        n_type = notif.object_type
        n_action = notif.action_type
        n_sender_id = notif.sender_id
        n_actor = notif.triggered_by.full_name

        #let's give each object a proper id so that ids of different_objects do not clash
        if n_type == 'poll':
            new_object_id = '{}_poll_{}'.format(n_object_id, n_action[:3])
        
        elif n_type == 'opinion':
            new_object_id = '{}_op_{}'.format(n_object_id, n_action[:3])

        elif n_type == 'comment':
            new_object_id = '{}_comm_{}'.format(n_object_id, n_action[:3])

        elif n_type == 'reply':
            new_object_id = '{}_rep_{}'.format(n_object_id, n_action[:3])

        elif n_type == 'share':
            new_object_id = '{}_share_{}'.format(n_object_id, n_action[:3])

        elif n_type == 'like':
            new_object_id = '{}_like_{}'.format(n_object_id, n_action[:3])

        elif n_type == 'follow':
            new_object_id = '{}_foll_{}'.format(n_object_id, n_action[:3])

    

        if new_object_id not in dictt.keys():
            dictt[new_object_id] = {}
            dictt[new_object_id] = {
                'unseen': False,
                
                'objectType': n_type,
                'objectOriginText': '',
                'objectId': new_object_id,
                'action': n_action,
                'leadingActors': [],
                'otherActors': [],            
            }


            if notif.status == 'unseen':
                dictt[new_object_id]['unseen'] = True
                unseen_notifications.append(notif.id)
             
            if n_type == 'poll':
                poll = request.dbsession.query(Poll).filter(Poll.id == n_object_id).first()
                dictt[new_object_id]['objectOriginText'] = poll.question
            
            elif n_type == 'opinion':
                opinion = request.dbsession.query(Opinion).filter(Opinion.id == n_object_id).first()
                dictt[new_object_id]['objectOriginText'] = opinion.opinion

            elif n_type ==  'comment':
                comment = request.dbsession.query(Comment).filter(Comment.id == n_object_id).first()
                dictt[new_object_id]['objectOriginText'] = comment.comment
                


            #follow notifications are a different ball of beans
            if n_type =='follow' and len(dictt[new_object_id]['leadingActors']) < 3:
                dictt[new_object_id]['leadingActors'].append(n_actor)

            elif n_type == 'follow' and len(dictt[new_object_id]['leadingActors']) > 3:
                dictt[new_object_id]['otherActors'].append(n_sender_id)

            #in cases other than a follow notification
            elif n_sender_id in user_followings(request, user_id) and len(dictt[new_object_id]['leadingActors']) < 3:
                dictt[new_object_id]['leadingActors'].append(n_actor)
            else:
                dictt[new_object_id]['otherActors'].append(n_sender_id)

        else:
            if notif.status == 'unseen':
                dictt[new_object_id]['unseen'] = True
                unseen_notifications.append(notif.id)

            if n_sender_id in user_followings(request, user_id) and len(dictt[new_object_id]['leadingActors']) < 3:
                dictt[new_object_id]['leadingActors'].append(n_actor)
            else:
                dictt[new_object_id]['otherActors'].append(n_sender_id)

    new = {"notifs": [], "notif_ids": [], "unseen": 0, 'unseenNotifs': unseen_notifications}


    for item in dictt.keys():
        leading_actors = dictt[item]['leadingActors']
        other_actors = dictt[item]['otherActors']
        notification_type = dictt[item]['action']
        object_type = dictt[item]['objectType']
        object_origin_text = dictt[item]['objectOriginText']
        unseen = dictt[item]['unseen']
        notification_text = ""
        

        if len(leading_actors) > 0:
            leading_actors = " , ".join(leading_actors)
            notification_text = leading_actors

        if len(other_actors) > 0:
            if notification_text:
                if len(other_actors) == 1:
                    notification_text += ' and <b>' + str(len(other_actors)) + 'other persons </b> '
                else:
                    notification_text += ' and <b>' + str(len(other_actors)) + ' others </b>'
            else:
                if len(other_actors) == 1:
                    notification_text = '<b>' + str(len(other_actors)) + ' person </b>'
                else:
                    notification_text= '<b>' + str(len(other_actors)) + ' people </b>'
      
        if object_type == 'follow':
            notification_text += notification_type + ' you'
        else:
            notification_text += notification_type + ' your ' + object_type + ': ' + object_origin_text

        notif_dictt = {'text': notification_text}

        new['notifs'].append(notif_dictt)
        new['notif_ids'] = notification_ids

        if unseen == True:
           new['unseen'] += 1





    return new
        

@view_config(route_name='mark_notifications_as_seen', renderer='json')
def mark_notifications_as_seen(request):
    notifications = request.json_body.get('notifications')

    notifications = notifications.split(',')

    notifications = request.dbsession.query(Notification).filter(Notification.id.in_(notifications))

    for notification in notifications: 
        notification.status = 'seen'
    transaction.commit()

if __name__ == '__main__':
    x = {"notifs": [{'1':{'action': 'liked'}}]}

    print (x['notifs'].keys())
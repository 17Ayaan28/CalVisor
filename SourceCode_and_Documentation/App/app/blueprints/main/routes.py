from . import main
from app import db
from app.modules.parsers import parse_events
import datetime
from app.Classes.Recommendation_System import Recommendation_System
from app.Classes.Models import Event, User, Invites, Accepted_Inviters, Scheduling_Invites
from app.Classes.Invitation_System import Invitation_System
from flask_login import login_required
from flask import render_template, session, redirect, url_for, current_app, request, Response
from flask_login import current_user
import json
from datetime import date
from datetime import datetime as dt
from .forms import NewEventForm, InviteForm, RecommendationForm, EditEventForm, ChangePrivacyForm, \
    ChangeUsernameForm, ChangeEmailForm, ChangeKnownPasswordForm,FormDefaults, DefaultDetails, ChangeDetailsForm


@main.route('/')
def home_page():
    return render_template('index.html')

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    all_events = parse_events(current_user.id)
    return render_template('dashboard.html', all_events=all_events)

@main.route('/search_username', methods=['GET', 'POST'])
@login_required
def search_username():

    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if user == None or user.profile_settings:
        return redirect(url_for('main.user_not_found', username=username))

    all_events = parse_events(user.id)
    return render_template('found_user.html', all_events=all_events, username=username)


@main.route('/user_not_found/<username>', methods=['GET'])
@login_required
def user_not_found(username):
    return render_template('no_user_found.html', username=username)

@main.route('/clear_all', methods= ['GET', 'POST'])
@login_required
def clear_all():
    all_events = Event.query.filter_by(user_id=current_user.id)
    for event in all_events:
        db.session.delete(event)
        db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html')


@main.route('/edit_details', methods=['GET', 'POST'])
@login_required
def edit_details():

    defaultDetails = DefaultDetails(email = current_user.email,
                                    username = current_user.username,
                                    password1 = current_user.password,
                                    password2 = current_user.password,
                                    privacy = current_user.profile_settings)
    form = ChangeDetailsForm(obj = defaultDetails)
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        current_user.password = form.password2.data
        current_user.profile_settings = form.privacy.data
        db.session.commit()

        return redirect(url_for('main.profile'))

    return render_template('change_details.html', form=form)


@main.route('/new_event', methods=['GET', 'POST'])
@login_required
def new_event():
    form = NewEventForm()
    if form.validate_on_submit():

        new_event = Event(name = form.name.data,
                          addr = form.addr.data,
                          date = form.date.data,
                          start_time = form.start_time.data,
                          end_time = form.end_time.data,
                          repeating_event = form.repeating_event.data,
                          user_id = current_user.id)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('main.new_event'))

    return render_template('new_event.html', form=form)

@main.route('/recommendations', methods=['GET', 'POST'])
@login_required
def recommendations():

    has_events_today = Event.query.filter_by(date=dt.now().date()).filter_by(user_id=current_user.id).all()
    has_events_before=False
    curr_time = dt.now().time()
    for event in has_events_today:
        if event.start_time <= curr_time:
            has_events_before = True

    return render_template('recommendations.html', has_events_before=str(has_events_before).lower())


@main.route('/get_recommendations', methods=['GET', 'POST'])
@login_required
def get_recommendations():

    # Get Body of HTTP Request
    body = request.json

    # Grab Variables from body
    have_place = body['have_place'] == 'Yes'
    destination = body['destination']
    category = body['category']
    hrs = int(body['hrs'])
    mins = int(body['mins'])
    total_dur = hrs * 60 + mins
    curr_loc = body['curr_loc']

    curr_date = dt.now().date()
    all_events = Event.query.filter_by(date=curr_date).filter_by(user_id=current_user.id).all()

    rec_sys = Recommendation_System()

    rec_dict = rec_sys.get_recs(all_events, total_dur, category, current_loc=curr_loc)

    return rec_dict, 200

@main.route('/schedule_place', methods=['GET', 'POST'])
@login_required
def schedule_place():

    # Get Body of HTTP Request
    body = request.json
    searched_place = body['destination']
    curr_loc = body['curr_loc']
    hrs = int(body['hrs'])
    mins = int(body['mins'])
    total_dur = hrs * 60 + mins

    rec_sys = Recommendation_System()

    rec = rec_sys.schedule_place(curr_loc, searched_place, total_dur)

    return rec, 200


@main.route('/add_rec', methods=['GET', 'POST'])
@login_required
def add_rec():

    start_time_str = request.args.get('rec_start')
    end_time_str = request.args.get('rec_end')

    start_time_obj = dt.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S").time()
    end_time_obj = dt.strptime(end_time_str, "%Y-%m-%dT%H:%M:%S").time()

    new_event = Event(name = request.args.get('rec_name'),
                      addr =request.args.get('rec_addr'),
                      date = dt.now().date(),
                      start_time = start_time_obj,
                      end_time = end_time_obj,
                      repeating_event = False,
                      user_id = current_user.id)
    db.session.add(new_event)
    db.session.commit()

    return redirect(url_for('main.dashboard'))


@main.route('/edit_event', methods=['GET', 'POST'])
@login_required
def edit_event():
    id = request.args.get('id')
    event = Event.query.filter_by(id=id).first()

    default_values = FormDefaults(name=event.name,
                                  addr=event.addr,
                                  date=event.date,
                                  start_time=event.start_time,
                                  end_time=event.end_time,
                                  repeating_event=event.repeating_event)

    form = NewEventForm(obj=default_values)
    if form.validate_on_submit():

        event.name = form.name.data
        event.addr = form.addr.data
        event.date = form.date.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.repeating_event = form.repeating_event.data
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('edit_event.html', event=event, form=form)


@main.route('/delete_event', methods=['GET', 'POST'])
@login_required
def delete_event():
    id = request.args.get('id')
    event = Event.query.filter_by(id=id).first()
    db.session.delete(event)
    db.session.commit()

    return redirect(url_for('main.dashboard'))


@main.route('/invite', methods=['POST']) #Invitation System
@login_required
def invite():
    content = request.get_json()

    if User.query.filter_by(username=content.get('username')).first() is None:
        response_content = {
            'message': "User Not Found! Please check your username"
        }
        return Response(json.dumps(response_content), mimetype='application/json')
    elif User.query.filter_by(username=content.get('username')).first().id == current_user.id:
        response_content = {
            'message': "Oops! You accidently invited yourself!"
        }
        return Response(json.dumps(response_content), mimetype='application/json')
    else:

        invitee_id = User.query.filter_by(username=content.get('username')).first().id
        inviter = User.query.filter_by(id=current_user.id).first()
        invitee_invites = Accepted_Inviters.query.filter_by(invitee_id=invitee_id).all()
        if invitee_invites is None or len(invitee_invites) == 0:

            new_invite = Invites(inviter_id=current_user.id,
                                 invitee_id=invitee_id,
                                 invitee_username=content.get('username'),
                                 event_id= int(content.get('event_id')))
            db.session.add(new_invite)
            db.session.commit()
        for invitee_invite in invitee_invites:
            if invitee_invite.inviter_username == inviter.username and invitee_invite.inviter_id == inviter.id:

                new_invite = Invites(inviter_id=current_user.id,
                                     invitee_id=invitee_id,
                                     invitee_username=content.get('username'),
                                     invite_accepted=True,
                                     event_id = int(content.get('event_id')))

                db.session.add(new_invite)
                db.session.commit()
                event_invited = Event.query.filter_by(id=int(content.get('event_id'))).first()
                invitee_day_events = Event.query.filter_by(user_id=invitee_id).filter_by(date=event_invited.date).all()
                invite_sys = Invitation_System()
                can_schedule, previous_event_id, next_event_id = invite_sys.find_time_gap(event_invited.start_time, event_invited.end_time, invitee_day_events)
                if can_schedule:
                    if previous_event_id == None:
                        previous_event_id = -1
                    if next_event_id == None:
                        next_event_id = -1
                    scheduling_event = Scheduling_Invites(invite_id=new_invite.id,
                                                          inviter_id=current_user.id,
                                                          invitee_id=invitee_id,
                                                          inviter_username=invitee_invite.inviter_username,
                                                          invitee_username=content.get('username'),
                                                          invite_name=event_invited.name,
                                                          invite_location_addr=event_invited.addr,
                                                          invite_date=event_invited.date,
                                                          invite_start_time=event_invited.start_time,
                                                          invite_end_time = event_invited.end_time,
                                                          invitee_next_event = next_event_id,
                                                          invitee_previous_event=previous_event_id,
                                                          inviter_approval=True)
                    db.session.add(scheduling_event)
                    db.session.commit()
                break
            else:

                new_invite = Invites(inviter_id=current_user.id,
                                     invitee_id=invitee_id,
                                     invitee_username=content.get('username'),
                                     event_id=int(content.get('event_id')))
                db.session.add(new_invite)
                db.session.commit()
        return Response('{"message": " "}', mimetype='application/json')

@main.route('/incoming_invites', methods=['GET'])  # Invitation System
@login_required
def incoming_invites():
    received_invites = Invites.query.filter_by(invitee_id=current_user.id)
    if received_invites is not None and received_invites.count() > 0:

        content = {'content': []}
        for received_invite in received_invites:
            if not received_invite.invite_accepted and not received_invite.invite_rejected:
                inviter = User.query.filter_by(id=received_invite.inviter_id).first().username
                message = inviter + " wants to invite you to an event! Would you like to accept the invite?"
                content_invite = {
                    'message': message,
                    'invite_id': received_invite.id
                }
                content['content'].append(content_invite)

        if len(content['content']) > 0:
            return Response(json.dumps(content), status=200, mimetype='application/json')
            # why is there a return inside the for loop? Was it like that before?
        else:

            modal_message = "You do not have any outstanding invites!"
            content_message = {
                'message': modal_message
            }
            return Response(json.dumps(content_message), status=200, mimetype='application/json')
    else:

        modal_message = "You do not have any outstanding invites!"
        content_message = {
            'message': modal_message
        }
        return Response(json.dumps(content_message), status=200, mimetype='application/json')


@main.route('/accept_invite', methods=['POST']) #Invitation System
@login_required
def accept_invite():

    content = request.get_json()
    invite_id = content.get('invite_id')
    event_id = content.get('event_id')

    accepted_invite = Invites.query.filter_by(id=invite_id).first()
    accepted_invite.invite_accepted = True
    accepted_invite.invite_rejected = False
    db.session.commit()
    event_id = accepted_invite.event_id

    invited_event = Event.query.filter_by(id=event_id).first()

    invitee = User.query.filter_by(id=current_user.id).first()
    inviter= User.query.filter_by(id=accepted_invite.inviter_id).first()
    accepted_inviter = Accepted_Inviters(invitee_id= current_user.id,
                                         inviter_id=accepted_invite.inviter_id,
                                         invitee_username=invitee.username,
                                         inviter_username=inviter.username)
    db.session.add(accepted_inviter)
    db.session.commit()
    invite_sys = Invitation_System()
    invitee_day_events = Event.query.filter_by(user_id=current_user.id).filter_by(date=invited_event.date).all()
    can_schedule, previous_event_id, next_event_id = invite_sys.find_time_gap(invited_event.start_time,
                                                                              invited_event.end_time,
                                                                              invitee_day_events)
    if can_schedule:
        if previous_event_id == None:
            previous_event_id = -1
        if next_event_id == None:
            next_event_id = -1
        scheduling_event = Scheduling_Invites(invite_id=invite_id,
                                              inviter_id=accepted_invite.inviter_id,
                                              invitee_id=accepted_invite.invitee_id,
                                              inviter_username=inviter.username,
                                              invitee_username=invitee.username,
                                              invite_name=invited_event.name,
                                              invite_location_addr=invited_event.addr,
                                              invite_date=invited_event.date,
                                              invite_start_time=invited_event.start_time,
                                              invite_end_time=invited_event.end_time,
                                              invitee_next_event=next_event_id,
                                              invitee_previous_event=previous_event_id,
                                              inviter_approval=True)
        db.session.add(scheduling_event)
        db.session.commit()
    return Response('{"message": " "}', mimetype='application/json')

@main.route('/decline_invite', methods=['POST']) #Invitation System
@login_required
def decline_invite():
    content = request.get_json()
    invite_id = content.get('invite_id')
    rejected_invite = Invites.query.filter_by(id=invite_id).first()
    rejected_invite.invite_accepted = False
    rejected_invite.invite_rejected = True
    db.session.commit()
    db.session.delete(rejected_invite)
    db.session.commit()
    return Response('{"message": " "}', mimetype='application/json')


@main.route('/scheduling_invites', methods=['GET']) #Invitation System
@login_required
def scheduling_invites():
    my_events_contents = []
    previous_events = []
    next_events = []
    my_events = Scheduling_Invites.query.filter_by(invitee_id=current_user.id).all()
    if my_events is not None and len(my_events) > 0:
        for my_event in my_events:
            if my_event.inviter_approval == True and my_event.invitee_approval == False:
                my_event_invite = Invites.query.filter_by(id=my_event.invite_id).first()
                if not my_event_invite.invite_accepted:

                    inviter = User.query.filter_by(id=my_event.inviter_id).first()
                invitee = User.query.filter_by(id=my_event.invitee_id).first()
                my_events_content = (inviter.username, invitee.username, my_event.id, my_event.invite_name, my_event.invite_location_addr,
                                     my_event.invite_date.strftime("%B %d, %Y"), my_event.invite_start_time.strftime("%I:%M %p"),
                                     my_event.invite_end_time.strftime("%I:%M %p"))
                my_events_contents.append(my_events_content)
                if my_event.invitee_previous_event != -1:
                    previous_event = Event.query.filter_by(id=my_event.invitee_previous_event).first()
                    previous_event_details = [previous_event.id, previous_event.name, previous_event.addr, previous_event.date.strftime("%B %d, %Y"),
                                              previous_event.start_time.strftime("%I:%M %p"),previous_event.end_time.strftime("%I:%M %p")]
                else:
                    previous_event_details = [-1,"", "", -1, -1, -1]
                if my_event.invitee_next_event != -1:
                    next_event = Event.query.filter_by(id=my_event.invitee_next_event).first()
                    next_event_details = [next_event.id, next_event.name, next_event.addr, next_event.date.strftime("%B %d, %Y"),
                                              next_event.start_time.strftime("%I:%M %p"),next_event.end_time.strftime("%I:%M %p")]
                else:
                    next_event_details = [-1,"", "", -1, -1, -1]
                next_events.append(next_event_details)
                previous_events.append(previous_event_details)


    return render_template('scheduling_event.html', my_events_contents=my_events_contents, previous_events=previous_events, next_events=next_events)

@main.route('/finalise_invite_accept', methods=['POST']) #Invitation System
@login_required
def finalise_invite_accept():
    content = request.get_json()
    scheduling_id = content.get('scheduling_id')
    scheduling_div = content.get('index')
    scheduling_invite = Scheduling_Invites.query.filter_by(id=scheduling_id).first()
    if scheduling_invite is not None:
        scheduling_invite.invitee_approval = True
        db.session.commit()
        new_event = Event(name=scheduling_invite.invite_name,
                          addr=scheduling_invite.invite_location_addr,
                          date=scheduling_invite.invite_date,
                          start_time=scheduling_invite.invite_start_time,
                          end_time=scheduling_invite.invite_end_time,
                          repeating_event= False,
                          user_id=scheduling_invite.invitee_id)
        db.session.add(new_event)
        db.session.commit()

        invite = Invites.query.filter_by(id=scheduling_invite.invite_id).first()
        db.session.delete(invite)
        db.session.commit()
        db.session.delete(scheduling_invite)
        db.session.commit()
        confirmation = {
            'message': "Event added"
        }
        return Response(json.dumps(confirmation), mimetype='application/json')
    else:
        confirmation = {
            'error_message': "Sorry something went wrong. We will fix it ASAP"
        }
        return Response(json.dumps(confirmation), mimetype='application/json')

@main.route('/finalise_decline_accept', methods=['POST']) #Invitation System
@login_required
def finalise_decline_accept():
    content = request.get_json()
    scheduling_id = content.get('scheduling_id')
    scheduling_div = content.get('index')
    scheduling_invite = Scheduling_Invites.query.filter_by(id=scheduling_id).first()
    if scheduling_invite is not None:
        scheduling_invite.invitee_approval = False
        db.session.commit()
        invite = Invites.query.filter_by(id=scheduling_invite.invite_id).first()
        db.session.delete(invite)
        db.session.commit()
        db.session.delete(scheduling_invite)
        db.session.commit()
        confirmation = {
            'message': "Event declined"
        }
        return Response(json.dumps(confirmation), mimetype='application/json')
    else:
        confirmation = {
            'error_message': "Sorry something went wrong. We will fix it ASAP"
        }
        return Response(json.dumps(confirmation), mimetype='application/json')

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Show, WatchList
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    # Retrieve the current user's watchlist
    watchlist = WatchList.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html', user=current_user, watchlist=watchlist)

@views.route('/add-show', methods=['POST'])
@login_required
def add_show():
    title = request.form.get('title')
    genre = request.form.get('genre')
    release_year = request.form.get('release_year')

    if not title or not genre or not release_year:
        flash('Please fill in all fields', 'error')
    else:
        # Add new show and watchlist entry
        new_show = Show(title=title, genre=genre, release_year=release_year)
        db.session.add(new_show)
        db.session.commit()

        new_watchlist = WatchList(user_id=current_user.id, show_id=new_show.id, status='Planned')
        db.session.add(new_watchlist)
        db.session.commit()

        flash('Show added to your watchlist!', 'success')

    return redirect(url_for('views.home'))

@views.route('/update-watchlist/<int:id>', methods=['POST'])
@login_required
def update_watchlist(id):
    watchlist_item = WatchList.query.get_or_404(id)
    watchlist_item.status = request.form.get('status', watchlist_item.status)

    db.session.commit()
    return redirect(url_for('views.home'))

@views.route('/delete-watchlist/<int:id>', methods=['POST'])
@login_required
def delete_watchlist(id):
    watchlist_item = WatchList.query.get_or_404(id)
    db.session.delete(watchlist_item)
    db.session.commit()
    return redirect(url_for('views.home'))

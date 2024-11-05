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
    rating = request.form.get('rating')  # Add rating field
    description = request.form.get('description')  # Add description field

    if not title or not genre or not release_year:
        flash('Please fill in all fields', 'error')
    else:
        # Add new show and watchlist entry
        new_show = Show(
            title=title, 
            genre=genre, 
            release_year=release_year, 
            rating=rating,  # Save rating
            description=description  # Save description
        )
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

# New route for editing a show
@views.route('/edit-show/<int:show_id>', methods=['GET', 'POST'])
@login_required
def edit_show(show_id):
    show = Show.query.get_or_404(show_id)

    if request.method == 'POST':
        show.title = request.form.get('title')
        show.genre = request.form.get('genre')
        show.release_year = request.form.get('release_year')
        show.rating = request.form.get('rating')
        show.description = request.form.get('description')

        db.session.commit()
        flash('Show details updated successfully!', 'success')
        return redirect(url_for('views.home'))

    return render_template('edit_show.html', show=show, user=current_user)  # Pass current_user to the template
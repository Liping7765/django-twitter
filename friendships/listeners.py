def friendship_changed(sender, instance, **kwargs):
    #import inside of the function to avoid loop dependency
    from friendships.services import FriendshipService
    FriendshipService.invalidate_following_cache(instance.from_user_id)
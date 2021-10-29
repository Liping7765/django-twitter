def profile_changed(sender, instance, **kwargs):
    # import within the function to void dependency issue
    from accounts.services import UserService
    UserService.invalidate_profile(instance.user_id)
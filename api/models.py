from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password


class Member(models.Model):
    """Application user model for chat members"""
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(default=timezone.now)
    
    # Properties required for DRF compatibility
    is_authenticated = True
    is_anonymous = False
    
    class Meta:
        ordering = ['username']
    
    def __str__(self):
        return self.username
    
    def set_password(self, raw_password):
        """Hash and set password"""
        self.password_hash = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Check if provided password matches stored hash"""
        return check_password(raw_password, self.password_hash)
    
    def has_perm(self, perm, obj=None):
        """Required for DRF permission classes"""
        return True
    
    def has_module_perms(self, app_label):
        """Required for DRF permission classes"""
        return True
    
    def update_last_seen(self):
        """Update last activity timestamp"""
        self.last_seen = timezone.now()
        self.save(update_fields=['last_seen'])


class Message(models.Model):
    """Chat message model"""
    author = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.author.username}: {self.text[:50]}"

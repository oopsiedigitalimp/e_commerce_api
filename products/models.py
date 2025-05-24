import uuid
from django.db import models
from django.db import transaction

class Product(models.Model):
    # id field is used for inner system usage in purpouse to keep all products unique and avoid conflicts
    # id field must not be seen/be used by user. For acces an object must be used article_number
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('ProductCategory', on_delete=models.PROTECT)
    stock = models.PositiveIntegerField(default=0)
    # article_number is a unique id wich serves for Users usage
    # must be automaticly genereated with category.letter_code and article_seq_number (example: ELSP-120, EL - ELectronics, SP - SmartPhones, 120 - product number)
    article_number = models.CharField(max_length=30, unique=True, blank=True)
    # assambling parameter for an article_number, unique id for its category
    article_seq_number = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}, price:{self.price}"
    
    def save(self, *args, **kwargs):
        if self.category.subcategories.exists():
            raise ValueError("You can't create product of parent category. You must choose exact category.")

        # Potential problem with "races" by simulteneous creation of products of one category
        if not self.article_seq_number:
            with transaction.atomic():
                prefix = self.category.get_full_letter_code()
                last = Product.objects.filter(category=self.category).order_by('-article_seq_number').first()
                self.article_seq_number = (last.article_seq_number + 1) if last else 0
                self.article_number = f"{prefix}-{self.article_seq_number}"
        super().save(*args, **kwargs)
    
    @property
    def in_stock(self):
        return self.stock > 0

class ProductCategory(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subcategories', on_delete=models.CASCADE)
    # Must be allways uppercase: TO DO: add function of product save()
    letter_code = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.name
    
    def get_ancestors(self, include_self=False):
        ancestors = []
        category = self

        if include_self == True:
            ancestors.insert(0, category)
        
        while category.parent:
            ancestors.insert(0, category.parent)
            category = category.parent

        return ancestors

    def get_descendants(self, include_self=False):
        descendants = []
        category = self

        def collect_children(cat):
            for child in cat.subcategories.all():
                descendants.append(child)
                collect_children(child)

        if include_self == True:
            descendants.append(category)
        
        collect_children(category)

        return descendants

    def get_full_letter_code(self):
        return ''.join(c.letter_code for c in self.get_ancestors(include_self=True))
    
    def get_full_path(self):
        return "/".join(c.name for c in self.get_ancestors(include_self=True))
from django.db import models
from accounts.models import CustomUser


# نموذج المتجر
class Store(models.Model):
    WILAYAS_CHOICES = [
        ("01", "Adrar"),
        ("02", "Chlef"),
        ("03", "Laghouat"),
        ("04", "Oum El Bouaghi"),
        ("05", "Batna"),
        ("06", "Béjaïa"),
        ("07", "Biskra"),
        ("08", "Béchar"),
        ("09", "Blida"),
        ("10", "Bouira"),
        ("11", "Tamanrasset"),
        ("12", "Tébessa"),
        ("13", "Tlemcen"),
        ("14", "Tiaret"),
        ("15", "Tizi Ouzou"),
        ("16", "Alger"),
        ("17", "Djelfa"),
        ("18", "Jijel"),
        ("19", "Sétif"),
        ("20", "Saïda"),
        ("21", "Skikda"),
        ("22", "Sidi Bel Abbès"),
        ("23", "Annaba"),
        ("24", "Guelma"),
        ("25", "Constantine"),
        ("26", "Médéa"),
        ("27", "Mostaganem"),
        ("28", "M'Sila"),
        ("29", "Mascara"),
        ("30", "Ouargla"),
        ("31", "Oran"),
        ("32", "El Bayadh"),
        ("33", "Illizi"),
        ("34", "Bordj Bou Arreridj"),
        ("35", "Boumerdès"),
        ("36", "El Tarf"),
        ("37", "Tindouf"),
        ("38", "Tissemsilt"),
        ("39", "El Oued"),
        ("40", "Khenchela"),
        ("41", "Souk Ahras"),
        ("42", "Tipaza"),
        ("43", "Mila"),
        ("44", "Aïn Defla"),
        ("45", "Naâma"),
        ("46", "Aïn Témouchent"),
        ("47", "Ghardaïa"),
        ("48", "Relizane"),
        ("49", "Timimoun"),
        ("50", "Bordj Badji Mokhtar"),
        ("51", "Ouled Djellal"),
        ("52", "Béni Abbès"),
        ("53", "In Salah"),
        ("54", "In Guezzam"),
        ("55", "Touggourt"),
        ("56", "Djanet"),
        ("57", "El M'Ghair"),
        ("58", "El Menia"),
    ]

    CATIGORY_CHOICES = [
        ('ملابس رجالية' , 'ملابس رجالية'),
        ('ملابس نسائية' , 'ملابس نسائية'),
        ('ملابس أطفال' , 'ملابس أطفال'),
        ('هواتف نقالة','هواتف نقالة'),
        ('إلكترونيات','إلكترونيات'),
        ('مطعم رقمي','مطعم رقمي'),
        ('صيدلي','صيدلي'),
        ('إكسسوارات', 'إكسسوارات'),
        ('سوبيرات' , 'سوبيرات')
    ]
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='stores')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='store_logos/', blank=True)
    wilaya = models.CharField(max_length=2, choices=WILAYAS_CHOICES)
    catigory = models.CharField(choices=CATIGORY_CHOICES , max_length=255)

    def __str__(self):
        return self.name


# نموذج المنتج
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


# نموذج الطلب
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'قيد المعالجة'),
        ('shipped', 'قيد التوصيل'),
        ('delivered', 'تم التوصيل'),
    )

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='client_orders')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    delivery_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


# نموذج عنصر الطلب
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


# نموذج السائق
class DeliveryPerson(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    wilaya = models.CharField(max_length=2, choices=Store.WILAYAS_CHOICES)
    vehicle_type = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.username
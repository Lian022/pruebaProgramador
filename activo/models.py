from django.db import models

#Nombre del proyecto

class Proyecto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

#Subetapa del proyecto (Numero de torre o estructura que conforme una fase del proyecto) proyecto=>subetapa

class Subetapa(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

    class Meta:
        unique_together = ('proyecto', 'nombre')

    def __str__(self):
        return f"{self.proyecto.nombre} - {self.nombre}"

#Valores al credito constructor, un credito Proyecto=>Credito  || Credito=>Proyecto

class Credito(models.Model):
    proyecto = models.OneToOneField(
        Proyecto,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    cupo_total = models.DecimalField(max_digits=15, decimal_places=2)
    porcentaje_max_desembolso = models.FloatField()
    periodo_inicial = models.PositiveIntegerField()
    periodo_final = models.PositiveIntegerField()
    tasa_interes_anual = models.FloatField()

    def __str__(self):
        return f"Crédito para {self.proyecto.nombre}"

#Movimiento financiero asociado a una subetapa (ingreso o costo) Subetapa=>MovimientoFinanciero || MovimientoFinanciero=>Subetapa

class MovimientoFinanciero(models.Model):
    subetapa = models.ForeignKey(Subetapa, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    periodo = models.PositiveIntegerField()
    concepto = models.CharField(max_length=10)

    def __str__(self):
        return (f"{self.subetapa.nombre} | Periodo {self.periodo}: "
                f"{self.get_concepto_display()} de {self.valor}")
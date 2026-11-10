from django.db import migrations, models


def converter_status_fechado(apps, schema_editor):
    Permanencia = apps.get_model("api", "Permanencia")
    Permanencia.objects.filter(status="FECHADO").update(status="FINALIZADO")


def reverter_status_finalizado(apps, schema_editor):
    Permanencia = apps.get_model("api", "Permanencia")
    Permanencia.objects.filter(status="FINALIZADO").update(status="FECHADO")


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="veiculo",
            old_name="tipo",
            new_name="marca",
        ),
        migrations.AlterField(
            model_name="veiculo",
            name="marca",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="vaga",
            name="numero",
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.RenameField(
            model_name="permanencia",
            old_name="data_entrada",
            new_name="data_hora_entrada",
        ),
        migrations.RenameField(
            model_name="permanencia",
            old_name="data_saida",
            new_name="data_hora_saida",
        ),
        migrations.RenameField(
            model_name="permanencia",
            old_name="valor",
            new_name="valor_total",
        ),
        migrations.AlterField(
            model_name="permanencia",
            name="valor_total",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=10,
                null=True,
            ),
        ),
        migrations.RunPython(
            converter_status_fechado,
            reverter_status_finalizado,
        ),
        migrations.AlterField(
            model_name="permanencia",
            name="status",
            field=models.CharField(
                choices=[
                    ("ABERTO", "Aberto"),
                    ("FINALIZADO", "Finalizado"),
                ],
                default="ABERTO",
                max_length=10,
            ),
        ),
    ]

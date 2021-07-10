# WIP

## Redshift connection guide
To connect to redshift, you need to configurate security group. For this:
- Go to you clauster info (left panel clauster) -> properies.
- At network and security VPC security group link.
- Go to "reglas de enytrada" y "reglas de salida".
- Edit rules, agregar regla. TCP personalizado,
    - use Mi IP . Or
    - 	0.0.0.0/0	Permite el acceso de HTTP entrante de cualquier dirección IPv4
    -   ::/0	Permite el acceso HTTP entrante desde cualquier dirección IPv6
     Guardar.
- Importante agregar reglas de enrada y salida. Esperar un poquito antes de probar.

[Use:](https://www.youtube.com/watch?v=zE7ptm3mnFQ) as references from minute 1:30 to 2:10.
## Redshift connection guide
To connect to redshift, you need to configurate the security group. For this:
- Search the 'Security Group' in the Search bar.
- Click the desaire security group.
- Add a new rule at inbound and outbound rules level with the following information: 
    - Port range: 5439
    - Type: Custom TCP
    - Source Type: Custom
    - Protocol: TCP
    - Source: 
        - 	For IPv4: 0.0.0.0/0	
        -   For IPv6: ::/0
    - Save
- This could take some minutes after changes take efect.

[Use:](https://www.youtube.com/watch?v=zE7ptm3mnFQ) as references from minute 1:30 to 2:10.
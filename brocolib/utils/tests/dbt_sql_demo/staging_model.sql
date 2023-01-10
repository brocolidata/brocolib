with source as (
    select * from {{ source('test_source', 'test_table') }}
),

prepared_source as (
    select 
        cast(registration_dttm as TIMESTAMP) as horodatage_enregistrement,
        cast(id as FLOAT) as ID,
        cast(first_name as STRING) as prenom,
        cast(last_name as STRING) as nom,
        cast(email as STRING) as email,
        cast(gender as STRING) as sexe,
        cast(ip_address as STRING) as adresse_IP,
        cast(cc as STRING) as commentaire,
        cast(country as STRING) as pays,
        cast(birthdate as STRING) as date_de_naissance,
        cast(salary as FLOAT) as salaire,
        cast(title as STRING) as metier,
        cast(comments as STRING) as commentaire,
        cast(month as STRING) as mois
    from source
)

select * from prepared_source

                    +------------------------+
                    |     HTTP (FastAPI)     |
                    |     Rabbit (AIOPika)   |
                    +------------+-----------+
                                 |
                     +-----------v------------+
                     |  Application Layer     |
                     |   (UseCases + UoW)     |
                     +-----------+------------+
                                 |
                +-------------------------------+
                |          Domain Layer         |
                |  (Entities, Protocols, Svc)   |
                +-------------------------------+
              ↙               ↓               ↘
      +-----------+   +---------------+   +--------------+
      | SQL Repo  |   | Redis Repo    |   | MinIO Client |
      | Adapter   |   | Adapter       |   | Adapter      |
      +-----------+   +---------------+   +--------------+

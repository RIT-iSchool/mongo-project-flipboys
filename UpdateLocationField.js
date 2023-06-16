const connection = new Mongo( `localhost:27017` ),
      db = connection.getDB( `Flipkart` ),
      tweetsColl = db.getCollection( `Products` );

      db.Products.updateMany(
        {},
        [
            {
                $set: {
                    location: {
                        $cond: {
                            if: { $or: [
                                { $eq: ["$Longitude", ""]},
                                { $eq: ["$Latitude", ""]},
                            ]},
                            then: null,
                            else: {
                                type: "Point",
                                coordinates: ["$Longitude", "$Latitude"]
                            }
                        }
                    }
                }
            },
            {
                $unset: ["Longitude", "Latitude"]
            }
        ]
    )
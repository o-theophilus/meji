# Todo

implement paystack payment webhook
https://webhook.site/17bf6a9c-8586-4d8f-9ab6-d0b56c8adb66



item_table:

key | options
---------------
1   | ["a", "b", "c"]
2   | ["d", "e", "a"]
3   | ["g", "h", "i"]



cur.execute("""
    SELECT *
    FROM item_table
    WHERE ARRAY[%s] @> item.tags;
""", (["a", "b"],))
output = cur.fetchall()



# Cookie-Clicker-Automation

The script launches https://cookieclicker.gg/, clicks the big cookies while buying upgrades or products once available.

The products (such as cursors) are statically created, so defining a list with the "product" + a number between 0 and 19 is enough to create references. For example:
```["product0", "product1", ..., product19]```

In the case of upgrades, the list is created dynamically given that these are not available until certain progression is made. Each iteration refreshes the list of upgrades and verifies their availability.

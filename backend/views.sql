
CREATE OR REPLACE VIEW `productview`AS
SELECT `products`.* ,
cast(`products`.`product_price` * (1 - `products`.`product_discount` / 100) AS decimal(10,2)) AS `product_discount_price`,
`categories`.*
FROM `products` JOIN `categories`
ON `products`.`product_categorie` = `categories`.`categorie_id`;


CREATE OR REPLACE VIEW `cartview` AS
SELECT `productview`.* , `cart`.* FROM `productview`, `cart`
WHERE `productview`.`product_id` = `cart`.`cart_product`
AND `cart`.`cart_order` = 0


CREATE OR REPLACE VIEW `ordersview` AS
SELECT `productview`.* , `cart`.`cart_pr_contity`, `orders`.*, `address`.*
FROM `productview`, `cart`, `orders`, `address`
WHERE `productview`.`product_id` = `cart`.`cart_product`
AND `cart`.`cart_order` = `orders`.`order_id`
AND `orders`.`order_address` = `address`.`address_id`
AND `cart`.`cart_order` != 0;
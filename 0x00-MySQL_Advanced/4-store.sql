-- Create the trigger
DELIMITER //
CREATE TRIGGER decrease_quantity_after_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    DECLARE order_item_id INT;
    DECLARE order_quantity INT;
    
    -- Get the item ID and quantity from the new order
    SELECT item_id, quantity
    INTO order_item_id, order_quantity
    FROM orders
    WHERE id = NEW.id;
    
    -- Decrease the quantity of the item in the items table
    UPDATE items
    SET quantity = quantity - order_quantity
    WHERE id = order_item_id;
END;
//
DELIMITER ;

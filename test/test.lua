--[[
- @module Test
- @brief This is a test file.
--]]

local m_test = {}

-- Method Test(s)

--[[
- @brief Does the thing. Seriously.
- @note If this does not do the thing, try again.
- @note Sometimes things just don't be like that when it do.
    - @param `string` What are we gonna do?
--]]
function m_test:do_thing(what)
    assert(type(what) == "string", "string expected, got: " .. type(what))
    print("We are going to do " .. tostring(what))
end

--[[
- @brief Gets milk from the store. Except it's all soup. You went to the soup store.
- @param `self` The `m_test` module table.
- @return `string` "Soup"
--]]
function m_test.get_milk(self)
    return "soup"
end

-- Function Test(s)

function hello_world()
    print("Hello World!")
end

local function yeet()
    print("Delete")
end

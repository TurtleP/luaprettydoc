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

--[[
- @brief Makes the module print 'Weeeeeee!' with text
- @param `text`: Text to add
--]]
function m_test:weee(text)
    assert(type(text) == "string", "string expected, got: " .. type(text))
    print("Weeeeeee! " .. tostring(text))
end

--[[
==========================
- Test `exclusion` tag
- https://github.com/TurtleP/luaprettydoc/issues/3
==========================
- @brief Prepares something.
- @note Here's some mental notes for myself.
- @exclude
--]]
function m_test:prepare()

end

--[[
==========================
- Test empty `brief` tag and random empty tag
==========================
- @brief
- @note
--]]
function m_test:async()

end

--[[
==========================
- Test definition tag
- https://github.com/TurtleP/luaprettydoc/issues/3
==========================
- @definition m_test:copy(b)
- @brief copies matrix values from another matrix
- @param a:`math.matrix` the matrix to copy into
- @param b:`math.matrix` the matrix to copy from
- @return `math.matrix` matrix `a` copied from `b`
]]
function m_test.copy(a, b)
    a[ 1] = b[ 1]
    a[ 2] = b[ 2]
    a[ 3] = b[ 3]
    a[ 4] = b[ 4]
    a[ 5] = b[ 5]
    a[ 6] = b[ 6]
    a[ 7] = b[ 7]
    a[ 8] = b[ 8]
    a[ 9] = b[ 9]
    a[10] = b[10]
    a[11] = b[11]
    a[12] = b[12]
    a[13] = b[13]
    a[14] = b[14]
    a[15] = b[15]
    a[16] = b[16]

    return a
end

-- Function Test(s)

function hello_world()
    print("Hello World!")
end

-- local functions do not get documented

local function yeet()
    print("Delete")
end

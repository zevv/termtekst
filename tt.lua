#!/usr/bin/lua

local function utf8(c)
   if c < 128 then
      return string.char(c)
   elseif c < 2048 then
      return string.char(192 + c/64, 128 + c%64)
   elseif c < 55296 or 57343 < c and c < 65536 then
      return string.char(224 + c/4096, 128 + c/64%64, 128 + c%64)
   elseif c < 1114112 then
      return string.char(240 + c/262144, 128 + c/4096%64, 128 + c/64%64, 128 + c%64)
   end
end


page = arg[1] or 100

json = require "json"
bit = require "bit"
band = bit.band

local fd = io.popen("curl -s http://teletekst-data.nos.nl/json/" .. page)
local j = fd:read("*a")
d = json.decode(j)

local ansi = {
	["black"] = "30",
	["red"] = "31",
	["green"] = "32",
	["yellow"] = "33",
	["blue"] = "34",
	["magenta"] = "35",
	["cyan"] = "36",
	["white"] = "37",
	["bg-black"] = "40",
	["bg-red"] = "41",
	["bg-green"] = "42",
	["bg-yellow"] = "43",
	["bg-blue"] = "44",
	["bg-magenta"] = "45",
	["bg-cyan"] = "46",
	["bg-white"] = "107",
}

local char = {
	--[0x03] = "~",
	--[0x10] = " ",
	--[0x07] = "'",
	--[0x0c] = "-",
	--[0x0f] = "~",
	--[0x15] = "|",
	--[0x18] = ",",
	--[0x1a] = "/",
	--[0x1c] = ",",
	--[0x20] = " ",
	--[0x2a] = "|",
	--[0x30] = "_",
	--[0x35] = "l",
	--[0x3c] = "_",
	--[0x3f] = "#",
}

for l in d.content:gmatch("[^\r\n]+") do

	l = l:gsub("<([^>]+)>", function(h)
		local o = "\027[1;37m"
		local cs = h:match('class="(.-)"') or ""
		for c in cs:gmatch("(%S+)") do
			if ansi[c] then o = o .. "\027[" .. ansi[c] .. "m" end
		end
		return o
	end)

	l = l:gsub("&#x(%x+);", function(n)
		n = tonumber(n, 16) - 0xf020
		if n >= 64 then n = n - 32 end
		local o = band(n, 33) + band(n, 2) * 4 + band(n, 4) / 2 + band(n, 8) * 2 + band(n, 16) / 4 
		return char[n] or utf8(0x2800 + o)
	end)

	io.write(l)
	io.write("\027[0m")
	io.write("\n")
end


-- vi: ft=lua ts=3 sw=3

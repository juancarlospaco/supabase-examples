import std/[os, strutils, httpclient]

type Client* = object
  base_path* = "https://utawmowgglsndawzxebx.supabase.co/rest/v1/"
  pg_range*  = [0, 1]
  http*      : HttpClient

proc newClient*(apikey: string): Client =
  result = Client()
  result.http = newHttpClient(headers = newHttpHeaders({"apiKey": apikey, "Authorization": "Bearer " & apikey}))

proc connect*(self: Client; path: string): string =
  self.http.getContent(path)

proc resultSet*(self: Client; path: string; pagination = false) =
  if pagination:
    self.http.headers["Range"] = $self.pg_range[0] & '-' & $self.pg_range[1]
  echo self.connect(path)

proc selectAll*(self: Client; table_name: string; pagination = false): auto =
    let apipath = self.base_path & table_name & "?select=*"
    self.resultSet(apipath, pagination)

proc selectColumns*(self: Client; table_name: string; pagination = false; cols: seq[string]) =
    let apipath = self.base_path & table_name & "?select=" & cols.join(",")
    self.resultSet(apipath, pagination)

proc main() =
  let client = newClient(getEnv"SUPABASE_KEY")
  client.selectAll("products")
  # client.selectColumns("products", @["id"])

when isMainModule:
  main()

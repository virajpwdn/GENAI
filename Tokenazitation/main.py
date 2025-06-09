import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o");

text = "Hello this is Virat";
token = enc.encode(text);

print("TOKENS", token);

decode = enc.decode(token);
print("DECODE: ", decode);
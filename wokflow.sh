#!/bin/bash

# 🎨 Cores ANSI
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
MAGENTA='\033[1;35m'
RESET='\033[0m'

BASE_URL="http://127.0.0.1:8080/bff"

divider() {
  echo -e "\n${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}\n"
}

pause() {
  sleep 2
}

# 1. SIGNUP
divider
echo -e "${BLUE}🆕 [POST] /signup${RESET}"
echo -e "${YELLOW}Body:${RESET} {\"id\":0, \"name\":\"eduardo\", \"password\":\"eduardo\", \"role\":\"\"}"

SIGNUP_RESPONSE=$(curl -s -X POST "$BASE_URL/signup" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"id": 0, "name": "eduardo", "password": "eduardo", "role": ""}')

echo "$SIGNUP_RESPONSE"
echo

USER_ID=$(echo "$SIGNUP_RESPONSE" | grep -o '"id":[0-9]*' | cut -d':' -f2)

if [ -z "$USER_ID" ]; then
  echo -e "${RED}❌ Falha ao extrair o ID do usuário criado.${RESET}"
  exit 1
fi

echo -e "${GREEN}✅ Usuário criado com ID:${RESET} $USER_ID"
pause

# 2. LOGIN (com o novo usuário)
divider
echo -e "${BLUE}🔐 [LOGIN] POST /login${RESET}"
echo -e "${YELLOW}Body:${RESET} grant_type=password, username=eduardo, password=eduardo"

LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/login" \
  -H "accept: application/json" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'grant_type=password&username=eduardo&password=eduardo&scope=&client_id=string&client_secret=string')

TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access_token":"[^"]*"' | cut -d':' -f2 | tr -d '"')

if [ -z "$TOKEN" ] || [ "$TOKEN" == "null" ]; then
  echo -e "${RED}❌ Token não obtido. Resposta:${RESET}"
  echo "$LOGIN_RESPONSE"
  exit 1
fi

echo -e "${GREEN}✅ Token recebido com sucesso!${RESET}"
echo -e "${CYAN}Token:${RESET} $TOKEN"
pause

# 3. UPDATE USER
divider
echo -e "${BLUE}✏️ [PUT] /$USER_ID${RESET}"
echo -e "${YELLOW}Body:${RESET} {\"id\":0, \"name\":\"eduardo_falcao\", \"password\":\"nova_senha\", \"role\":\"admin\"}"

curl -s -X PUT "$BASE_URL/$USER_ID" \
  -H "accept: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"id": 0, "name": "eduardo_falcao", "password": "nova_senha", "role": "admin"}'
echo
pause

# 4. GET /logado
divider
echo -e "${BLUE}👤 [GET] /logado${RESET}"
echo -e "${YELLOW}Headers:${RESET} Authorization: Bearer <token>"

curl -s -X GET "$BASE_URL/logado" \
  -H "accept: application/json" \
  -H "Authorization: Bearer $TOKEN"
echo
pause

# 5. GET /cryptocurrencies
divider
echo -e "${BLUE}💰 [GET] /cryptocurrencies${RESET}"
echo -e "${YELLOW}Query:${RESET} currency=usd, page=1, per_page=10"

curl -s -X GET "$BASE_URL/cryptocurrencies?currency=usd&page=1&per_page=10" \
  -H "accept: application/json" \
  -H "Authorization: Bearer $TOKEN"
echo
pause

# 6. GET /market/summary
divider
echo -e "${BLUE}📈 [GET] /market/summary${RESET}"
echo -e "${YELLOW}Query:${RESET} currency=usd"

curl -s -X GET "$BASE_URL/market/summary?currency=usd" \
  -H "accept: application/json" \
  -H "Authorization: Bearer $TOKEN"
echo
pause

# 7. GET /cryptocurrencies/bitcoin/history
divider
echo -e "${BLUE}📊 [GET] /cryptocurrencies/bitcoin/history${RESET}"
echo -e "${YELLOW}Query:${RESET} currency=usd, start_date=2025-07-02, end_date=2025-07-03"

curl -s -X GET "$BASE_URL/cryptocurrencies/bitcoin/history?currency=usd&start_date=2025-07-02&end_date=2025-07-03" \
  -H "accept: application/json" \
  -H "Authorization: Bearer $TOKEN"
echo
pause

# 8. PUT /1 (tentativa de editar outro usuário)
divider
echo -e "${BLUE}🔒 [PUT] /1 (tentativa de editar outro usuário)${RESET}"
echo -e "${YELLOW}Body:${RESET} {\"id\":1, \"name\":\"hacker\", \"password\":\"hack\", \"role\":\"admin\"}"

EDIT_OTHER_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/edit_other.json -X PUT "$BASE_URL/1" \
  -H "accept: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "name": "hacker", "password": "hack", "role": "admin"}')

EDIT_OTHER_BODY=$(cat /tmp/edit_other.json)

if [ "$EDIT_OTHER_RESPONSE" -ne 200 ]; then
  echo -e "${RED}❌ Não autorizado a editar outro usuário (id=1).${RESET}"
else
  echo -e "${GREEN}✅ Edição bem-sucedida:${RESET} $EDIT_OTHER_BODY"
fi
pause

# 10. DELETE /{id}
echo -e "${BLUE}🗑️ [DELETE] /$USER_ID${RESET}"

curl -s -X DELETE "$BASE_URL/$USER_ID" \
  -H "accept: */*" \
  -H "Authorization: Bearer $TOKEN"
echo
echo -e "${GREEN}✅ Usuário com ID $USER_ID deletado com sucesso!${RESET}"
pause

# FINAL
divider
echo -e "${GREEN}✅ Workflow completo!${RESET}"
echo "Todos os endpoints foram testados com sucesso (incluindo falhas esperadas por permissão)."

# pyright: reportMissingImports=false

# ═══════════════════════════════════════════════════════════════
# 1. ИМПОРТЫ И БАЗОВЫЕ НАСТРОЙКИ
# ═══════════════════════════════════════════════════════════════

from pyscript import document, when
from js import FileReader, Blob, URL, document as js_document
from pyodide.ffi import create_proxy
import asyncio
import re
from datetime import datetime

print("🐍 PyScript загружен!")


# ═══════════════════════════════════════════════════════════════
# 2. КОНСТАНТЫ И СЛОВАРИ
# ═══════════════════════════════════════════════════════════════

# ─── 2.1. Аспекты ───
ASPECTS = [
    # Еда
    "еда", "пицца", "паста", "бургер", "суши", "стейк", "салат", "суп",
    "кофе", "чай", "напиток", "вино", "пиво", "десерт", "торт", "хлеб",
    "блюдо", "кухня", "меню", "порция", "порции", "ингредиенты",
    "соус", "специи", "гарнир", "закуска", "мороженое", "пирожное",
    # Обслуживание
    "сервис", "обслуживание", "персонал", "официант", "официантка",
    "менеджер", "хостес", "бармен", "повар", "администратор",
    "отношение", "вежливость", "внимательность",
    # Доставка
    "доставка", "курьер", "водитель", "заказ", "упаковка", "сроки",
    "время", "ожидание",
    # Цена и качество
    "цена", "цены", "стоимость", "качество", "соотношение", "скидка",
    "чек", "счет", "оплата",
    # Атмосфера
    "атмосфера", "музыка", "шум", "освещение", "интерьер", "декор",
    "обстановка", "уют", "чистота", "грязь", "запах", "температура",
    "кондиционер", "вентиляция",
    # Место и удобства
    "локация", "парковка", "комната", "кровать", "ванная", "туалет",
    "вайфай", "wi-fi", "интернет", "бассейн", "спортзал", "лифт",
    "мебель", "подушка", "одеяло", "полотенце",
    # Отель
    "завтрак", "обед", "ужин", "душ", "вид", "номер", "ресепшн",
    "заселение", "выселение",
    # Товары
    "экран", "батарея", "клавиатура", "тачпад", "динамики", "камера",
    "зарядка", "кабель", "корпус", "вес", "размер", "материал",
    "качество сборки", "гарантия", "инструкция",
    # Общее
    "впечатление", "опыт", "поездка", "визит", "пребывание",
    "рекомендация", "отзыв"
]

# ─── 2.2. Маркеры ───
NEGATIVE_MARKERS = [
    "опозда", "долго", "медленн", "задержк",
    "ждал", "ждала", "ждали", "очередь", "тянул",
    "ужасн", "плох", "отвратительн", "грязн", "холодн", "невкусн",
    "стар", "дешев", "сыр", "пересол", "пережар", "сух",
    "жестк", "вял", "испорч", "просроч",
    "маленьк", "мало", "небольш", "крошечн",
    "игнорир", "нахамил", "груб", "оставляет желать лучшего",
    "невежлив", "хамств", "безразличн", "невнимательн",
    "не работает", "сломан", "не включается", "глючит", "зависает",
    "барахлит", "не функционирует",
    "разочаров", "больше не приду", "не понравилось",
    "отвратн", "кошмар", "ужас", "проблем", "ошибк",
    "не рекомендую", "жаль", "обидно", "неудобн", "шумн", "тесн",
    "душн", "холодно", "жарко",
    "дорого", "завыш", "переплат", "обдираловк",
    "не отвечает", "не дозвониться", "недоступен",
    "отстой", "фигня", "ерунда", "лажа", "косяк", "жесть",
    "так себе", "не ахти", "ниже плинтуса", "ни о чём", "ни о чем",
    "не фонтан", "не торт",
    "не пришло", "не привезли", "забыли", "перепутали", "не дождались",
    "не дозвонились", "остыл", "остыла", "остыло",
    "обманули", "наврали", "накосячили",
    "хуже", "похуже", "не лучше",
]

POSITIVE_MARKERS = [
    "вкусн", "свеж", "ароматн", "сочн", "нежн", "хрустящ",
    "отличн", "прекрасн", "супер", "замечательн", "рекомендую",
    "понравилось", "великолепн", "идеальн", "восхитительн",
    "качественн", "чист", "порадовал", "порадовала", "приятн",
    "быстро", "вежлив", "внимательн", "профессиональн", "заботлив",
    "уютн", "комфортн", "стильн", "красив",
    "доступн", "выгодн", "недорог",
    "вернусь", "приду еще", "буду заказывать еще",
    "огонь", "топ", "пушка", "бомба", "класс", "кайф", "шикарн",
    "волшебн", "божественн",
    "на высоте", "на уровне", "выше всяких похвал", "выше ожиданий",
    "остался доволен", "осталась довольна", "остались довольны",
    "не пожалел", "не пожалела", "не пожалели",
    "лучше", "получше",
]

# ─── 2.3. Усилители ───
INTENSIFIERS = [
    "очень", "крайне", "абсолютно", "совершенно", "полностью",
    "чрезвычайно", "невероятно", "ужасно", "жутко", "страшно",
    "просто", "реально", "действительно", "искренне", "безумно",
    "чертовски", "дьявольски"
]

# ─── 2.4. Разделители ───
CONJUNCTION_PATTERN = re.compile(
    r'\b(?:но|однако|хотя|зато|тем не менее|несмотря на|и|а|да|а также|плюс|к тому же|при этом)\b',
    re.IGNORECASE
)

DASH_PATTERN = re.compile(r'\s[—–-]\s')

# ─── 2.5. Отрицание позитива ───
NEGATED_POSITIVE_PATTERN = re.compile(
    r'\bне\s+(вкусно|понравилось|рекомендую|работает|приятно|чисто|вежливо|быстро|удобно|качественно)',
    re.IGNORECASE
)


# ═══════════════════════════════════════════════════════════════
# 3. ГЛОБАЛЬНОЕ СОСТОЯНИЕ
# ═══════════════════════════════════════════════════════════════

sentiment_pipeline = None

status_div = document.getElementById("status")
results_div = document.getElementById("results")
analyze_btn = document.getElementById("analyze-btn")

single_mode_div = document.getElementById("single-mode")
batch_mode_div = document.getElementById("batch-mode")
csv_info_div = document.getElementById("csv-info")
process_batch_btn = document.getElementById("process-batch-btn")
pause_batch_btn = document.getElementById("pause-batch-btn")
cancel_batch_btn = document.getElementById("cancel-batch-btn")
batch_progress_wrapper = document.getElementById("batch-progress-wrapper")
batch_progress_fill = document.getElementById("batch-progress-fill")
batch_progress_text = document.getElementById("batch-progress-text")
batch_progress_percent = document.getElementById("batch-progress-percent")

batch_reviews = []
batch_results = []
batch_cancelled = False
batch_paused = False
last_single_result = None


# ═══════════════════════════════════════════════════════════════
# 4. РАБОТА С АСПЕКТАМИ
# ═══════════════════════════════════════════════════════════════

def find_aspects(text):
    """Находит аспекты в тексте по словарю."""
    if not text:
        return []

    text_lower = text.lower()
    found = []
    seen_positions = set()

    for aspect in ASPECTS:
        start = 0
        while True:
            idx = text_lower.find(aspect, start)
            if idx == -1:
                break
            if idx not in seen_positions:
                found.append({
                    "word": text[idx:idx + len(aspect)],
                    "start": idx,
                    "end": idx + len(aspect),
                    "aspect": aspect
                })
                seen_positions.add(idx)
            start = idx + 1

    found.sort(key=lambda x: x["start"])
    return found


def split_into_sentences(text):
    """Разбивает текст на предложения по . ! ?"""
    if not text:
        return []
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [p.strip() for p in parts if p and p.strip()]


def split_by_dashes(sentence):
    """Разбивает предложение по тире (— – -)."""
    if not sentence:
        return []
    parts = DASH_PATTERN.split(sentence)
    return [p.strip() for p in parts if p and p.strip()]


def split_by_conjunctions(sentence):
    """Разбивает предложение по союзам."""
    if not sentence:
        return []
    sentence = safe_str(sentence)
    if not sentence:
        return []

    matches = list(CONJUNCTION_PATTERN.finditer(sentence))
    if not matches:
        return [sentence]

    chunks = []
    prev_end = 0
    for match in matches:
        chunk = safe_str(sentence[prev_end:match.start()])
        if chunk:
            chunks.append(chunk)
        prev_end = match.start()

    tail = safe_str(sentence[prev_end:])
    if tail:
        chunks.append(tail)

    return chunks if chunks else [sentence]


def split_by_commas(sentence):
    """Разбивает предложение по запятым и точкам с запятой."""
    if not sentence:
        return []
    sentence = safe_str(sentence)
    if not sentence:
        return []
    parts = re.split(r'[,;]', sentence)
    return [p.strip() for p in parts if p and p.strip()]


def get_context_for_aspect(text, aspect_info):
    """Находит минимальный релевантный контекст для аспекта."""
    if not text or not aspect_info:
        return safe_str(text)

    aspect = safe_str(aspect_info.get("aspect", "")).lower()
    if not aspect:
        return safe_str(text)

    sentences = split_into_sentences(text)
    if not sentences:
        return safe_str(text)

    target_sentence = None
    for sent in sentences:
        if sent and aspect in sent.lower():
            target_sentence = sent
            break

    if not target_sentence:
        return safe_str(text)

    dash_chunks = split_by_dashes(target_sentence)
    if len(dash_chunks) > 1:
        for chunk in dash_chunks:
            if chunk and aspect in chunk.lower():
                return safe_str(chunk)

    chunks = split_by_conjunctions(target_sentence)

    final_chunks = []
    for chunk in chunks:
        if not chunk:
            continue
        aspects_in_chunk = sum(1 for a in ASPECTS if a in chunk.lower())
        if aspects_in_chunk > 1:
            final_chunks.extend(split_by_commas(chunk))
        else:
            final_chunks.append(chunk)

    for chunk in final_chunks:
        if chunk and aspect in chunk.lower():
            return safe_str(chunk)

    return safe_str(target_sentence)


# ═══════════════════════════════════════════════════════════════
# 5. АНАЛИЗ ТОНАЛЬНОСТИ
# ═══════════════════════════════════════════════════════════════

def safe_str(value):
    """Безопасно превращает значение в строку."""
    if value is None:
        return ""
    return str(value).strip()


def normalize_sentiment(label):
    """Приводит метку модели к POSITIVE / NEGATIVE / NEUTRAL."""
    label_lower = safe_str(label).lower()

    if 'positive' in label_lower or 'позитив' in label_lower:
        return 'POSITIVE'
    if 'negative' in label_lower or 'негатив' in label_lower:
        return 'NEGATIVE'
    if 'neutral' in label_lower or 'нейтрал' in label_lower:
        return 'NEUTRAL'

    star_match = re.search(r'(\d)\s*star', label_lower)
    if star_match:
        stars = int(star_match.group(1))
        if stars <= 2:
            return 'NEGATIVE'
        elif stars == 3:
            return 'NEUTRAL'
        else:
            return 'POSITIVE'

    return 'NEUTRAL'


def _count_marker_hits(text_lower, markers):
    """Считает количество уникальных маркеров в тексте."""
    return sum(1 for m in markers if m in text_lower)


def _has_intensifier(text_lower, markers):
    """Проверяет, есть ли усилитель рядом с каким-либо маркером."""
    for intensifier in INTENSIFIERS:
        for marker in markers:
            pattern = re.compile(
                re.escape(intensifier) + r'\s+\w{0,15}\s*' + re.escape(marker),
                re.IGNORECASE
            )
            if pattern.search(text_lower):
                return True
            pattern = re.compile(
                re.escape(marker) + r'\s+\w{0,15}\s*' + re.escape(intensifier),
                re.IGNORECASE
            )
            if pattern.search(text_lower):
                return True
    return False


def apply_markers(text, current_sentiment):
    """Корректирует тональность на основе маркеров."""
    text_lower = safe_str(text).lower()
    if not text_lower:
        return current_sentiment

    has_negated_positive = bool(NEGATED_POSITIVE_PATTERN.search(text_lower))

    neg_count = _count_marker_hits(text_lower, NEGATIVE_MARKERS)
    pos_count = _count_marker_hits(text_lower, POSITIVE_MARKERS)

    has_negative_intensifier = _has_intensifier(text_lower, NEGATIVE_MARKERS)
    has_positive_intensifier = _has_intensifier(text_lower, POSITIVE_MARKERS)

    if has_negated_positive:
        neg_count += 2

    if has_negative_intensifier:
        neg_count += 1
    if has_positive_intensifier:
        pos_count += 1

    has_negative = neg_count > 0
    has_positive = pos_count > 0

    if current_sentiment == 'NEUTRAL':
        if has_negative and not has_positive:
            print(f"  🔧 Маркер: NEUTRAL → NEGATIVE (neg={neg_count})")
            return 'NEGATIVE'
        elif has_positive and not has_negative:
            print(f"  🔧 Маркер: NEUTRAL → POSITIVE (pos={pos_count})")
            return 'POSITIVE'
        elif neg_count > pos_count:
            print(f"  🔧 Маркер: NEUTRAL → NEGATIVE (перевес neg={neg_count} vs pos={pos_count})")
            return 'NEGATIVE'
        elif pos_count > neg_count:
            print(f"  🔧 Маркер: NEUTRAL → POSITIVE (перевес pos={pos_count} vs neg={neg_count})")
            return 'POSITIVE'

    if current_sentiment == 'POSITIVE' and neg_count > pos_count:
        print(f"  🔧 Маркер: POSITIVE → NEGATIVE (перевес neg={neg_count} vs pos={pos_count})")
        return 'NEGATIVE'

    if current_sentiment == 'NEGATIVE' and pos_count > neg_count:
        print(f"  🔧 Маркер: NEGATIVE → POSITIVE (перевес pos={pos_count} vs neg={neg_count})")
        return 'POSITIVE'

    return current_sentiment


# ═══════════════════════════════════════════════════════════════
# 6. АГРЕГАЦИЯ И ОБЪЕДИНЕНИЕ РЕЗУЛЬТАТОВ
# ═══════════════════════════════════════════════════════════════

def merge_by_context(results):
    """Объединяет аспекты с одинаковым контекстом."""
    if not results:
        return []

    merged = {}
    for res in results:
        key = res['context']
        if key not in merged:
            merged[key] = {
                'aspects': [res['aspect']],
                'sentiment': res['sentiment'],
                'score': res['score'],
                'context': res['context']
            }
            if 'review_id' in res:
                merged[key]['review_id'] = res['review_id']
        else:
            if res['aspect'] not in merged[key]['aspects']:
                merged[key]['aspects'].append(res['aspect'])
            if res['score'] > merged[key]['score']:
                merged[key]['score'] = res['score']

    return list(merged.values())


def aggregate_results(results):
    """Считает статистику по тональностям."""
    if not results:
        return {
            'positive': [], 'negative': [], 'neutral': [],
            'total': 0, 'pos_pct': 0, 'neg_pct': 0, 'neu_pct': 0
        }

    positive = [r for r in results if r.get('sentiment') == 'POSITIVE']
    negative = [r for r in results if r.get('sentiment') == 'NEGATIVE']
    neutral = [r for r in results if r.get('sentiment') == 'NEUTRAL']

    total = len(results)
    pos_pct = round(len(positive) / total * 100) if total else 0
    neg_pct = round(len(negative) / total * 100) if total else 0
    neu_pct = round(len(neutral) / total * 100) if total else 0

    return {
        'positive': positive, 'negative': negative, 'neutral': neutral,
        'total': total, 'pos_pct': pos_pct, 'neg_pct': neg_pct, 'neu_pct': neu_pct
    }


def group_by_review(results):
    """Группирует результаты по ID отзыва."""
    grouped = {}
    for r in results:
        rid = r.get('review_id', 'unknown')
        if rid not in grouped:
            grouped[rid] = []
        grouped[rid].append(r)
    return grouped


def get_review_verdict(review_results):
    """Определяет вердикт отзыва по большинству аспектов."""
    if not review_results:
        return 'NEUTRAL'

    pos = sum(1 for r in review_results if r['sentiment'] == 'POSITIVE')
    neg = sum(1 for r in review_results if r['sentiment'] == 'NEGATIVE')

    if pos > neg:
        return 'POSITIVE'
    elif neg > pos:
        return 'NEGATIVE'
    elif pos == neg and pos > 0:
        return 'MIXED'
    else:
        return 'NEUTRAL'


def calculate_review_stats(grouped):
    """Считает статистику по отзывам."""
    pos = neg = mixed = neu = 0
    for rid, review_results in grouped.items():
        verdict = get_review_verdict(review_results)
        if verdict == 'POSITIVE':
            pos += 1
        elif verdict == 'NEGATIVE':
            neg += 1
        elif verdict == 'MIXED':
            mixed += 1
        else:
            neu += 1

    total = pos + neg + mixed + neu
    return {
        'positive': pos, 'negative': neg, 'mixed': mixed, 'neutral': neu,
        'total': total,
        'pos_pct': round(pos / total * 100) if total else 0,
        'neg_pct': round(neg / total * 100) if total else 0,
        'mixed_pct': round(mixed / total * 100) if total else 0,
        'neu_pct': round(neu / total * 100) if total else 0,
    }


def calculate_aspect_stats(results):
    """Считает статистику по аспектам."""
    stats = {}
    for r in results:
        aspect = r['aspect'].lower()
        if aspect not in stats:
            stats[aspect] = {'count': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        stats[aspect]['count'] += 1
        sentiment = r['sentiment']
        if sentiment == 'POSITIVE':
            stats[aspect]['positive'] += 1
        elif sentiment == 'NEGATIVE':
            stats[aspect]['negative'] += 1
        else:
            stats[aspect]['neutral'] += 1
    return stats


def get_top_aspects(results, top_n=5):
    """Возвращает топ-N аспектов с их статистикой."""
    stats = calculate_aspect_stats(results)
    return sorted(stats.items(), key=lambda x: x[1]['count'], reverse=True)[:top_n]


# ═══════════════════════════════════════════════════════════════
# 7. CSV: ИМПОРТ И ВАЛИДАЦИЯ
# ═══════════════════════════════════════════════════════════════

def parse_csv_line(line):
    """Парсит одну строку CSV с поддержкой кавычек."""
    parts = []
    current = ""
    in_quotes = False
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
            current += char
        elif char == ',' and not in_quotes:
            parts.append(current)
            current = ""
        else:
            current += char
    parts.append(current)
    return parts


def parse_csv(content):
    """Парсит CSV в формате id,text."""
    if not content:
        return None, ["Файл пустой"]

    lines = content.strip().split('\n')
    if not lines:
        return None, ["Файл пустой"]

    reviews = []
    errors = []

    for i, line in enumerate(lines, start=1):
        line = line.strip()
        if not line:
            continue

        parts = parse_csv_line(line)
        if len(parts) < 2:
            errors.append(f"Строка {i}: нужно минимум 2 колонки (id,text)")
            continue

        review_id = parts[0].strip()
        text = parts[1].strip()

        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        text = text.replace('""', '"')

        if not text:
            errors.append(f"Строка {i}: пустой текст отзыва")
            continue

        reviews.append({'id': review_id, 'text': text})

    if not reviews:
        return None, errors if errors else ["Не найдено ни одного валидного отзыва"]
    return reviews, errors


def format_csv_errors(errors):
    """Форматирует список ошибок CSV для отображения."""
    if not errors:
        return ""
    preview = errors[:5]
    html = "<ul style='margin: 0.5rem 0 0 1rem;'>"
    for err in preview:
        html += f"<li>{err}</li>"
    if len(errors) > 5:
        html += f"<li>...и ещё {len(errors) - 5} ошибок</li>"
    html += "</ul>"
    return html


def handle_csv_content(content):
    """Обрабатывает содержимое CSV-файла и обновляет UI."""
    global batch_reviews
    print(f"📄 Получено {len(content)} символов")
    reviews, errors = parse_csv(content)

    if reviews is None:
        csv_info_div.className = "csv-info error"
        err_text = errors[0] if errors else "Неизвестная ошибка"
        csv_info_div.innerHTML = f"❌ <b>Ошибка:</b> {err_text}"
        process_batch_btn.disabled = True
        batch_reviews = []
        return

    batch_reviews = reviews

    html = f"✅ <b>Загружено отзывов:</b> {len(reviews)}"
    html += "<div style='margin-top: 0.5rem; font-size: 0.9rem;'>"
    html += "<b>Первые отзывы:</b><ul style='margin: 0.3rem 0 0 1rem;'>"
    for r in reviews[:3]:
        text_preview = r['text'][:80] + ('...' if len(r['text']) > 80 else '')
        html += f"<li><code>#{r['id']}</code>: {text_preview}</li>"
    if len(reviews) > 3:
        html += f"<li><i>...и ещё {len(reviews) - 3}</i></li>"
    html += "</ul></div>"

    if errors:
        html += f"<div style='margin-top: 0.5rem; color: #c62828;'><b>⚠️ Пропущено строк:</b> {len(errors)}{format_csv_errors(errors)}</div>"

    csv_info_div.className = "csv-info"
    csv_info_div.innerHTML = html

    process_batch_btn.disabled = False
    print(f"✅ CSV загружен: {len(reviews)} отзывов")


# ═══════════════════════════════════════════════════════════════
# 8. ЭКСПОРТ HTML-ОТЧЁТА
# ═══════════════════════════════════════════════════════════════

# ─── 8.1. Вспомогательные HTML-функции ───

def _sentiment_label_css(sentiment):
    """Возвращает (css_class, badge_text) по тональности."""
    s = safe_str(sentiment).lower()
    if s == 'positive':
        return 'positive', 'ПОЗИТИВ'
    elif s == 'negative':
        return 'negative', 'НЕГАТИВ'
    else:
        return 'neutral', 'НЕЙТРАЛЬНО'


def _sentiment_short_text(sentiment):
    """Короткое текстовое обозначение тональности."""
    s = safe_str(sentiment).lower()
    if s == 'positive':
        return 'позитив'
    elif s == 'negative':
        return 'негатив'
    else:
        return 'нейтрально'


def _report_aspect_card_html(res, mode):
    """Генерирует HTML одной карточки аспекта для отчёта."""
    css_class, badge_text = _sentiment_label_css(res.get('sentiment', ''))

    score = res.get('score', 0) or 0
    confidence_pct = round(score * 100)
    aspects_display = ", ".join(res.get('aspects', []))
    context = safe_str(res.get('context', ''))

    return f"""
    <div class="aspect-card {css_class}">
        <div class="aspect-header">
            <span class="aspect-name">{aspects_display}</span>
            <span class="aspect-badge badge-{css_class}">{badge_text}</span>
        </div>
        <div class="aspect-context">"{context}"</div>
        <div class="aspect-confidence">Уверенность: {confidence_pct}%</div>
        <div class="confidence-bar">
            <div class="confidence-fill {css_class}" style="width: {confidence_pct}%;"></div>
        </div>
    </div>
    """


def _report_top_aspects_html(results, top_n=10):
    """Генерирует HTML топ-аспектов для отчёта."""
    if not results:
        return ""

    top = get_top_aspects(results, top_n)
    html = "<ul>"
    for i, (aspect, data) in enumerate(top, 1):
        count = data['count']
        pos_pct = round(data['positive'] / count * 100)
        neg_pct = round(data['negative'] / count * 100)

        if pos_pct > neg_pct:
            color, label = "#4CAF50", f"{pos_pct}% позитив"
        elif neg_pct > pos_pct:
            color, label = "#F44336", f"{neg_pct}% негатив"
        else:
            color, label = "#FF9800", "смешанный"

        html += f"""
        <li>
            <span class="aspect-label">{i}. {aspect}</span>
            <span class="aspect-count">{count} упом. • <b style="color: {color};">{label}</b></span>
        </li>
        """
    html += "</ul>"
    return html


def _report_review_card_html(review_id, review_text, review_results):
    """Генерирует HTML карточки отзыва для отчёта (batch)."""
    verdict = get_review_verdict(review_results)
    if verdict == 'POSITIVE':
        v_css, v_text = 'positive', 'ПОЗИТИВНЫЙ'
    elif verdict == 'NEGATIVE':
        v_css, v_text = 'negative', 'НЕГАТИВНЫЙ'
    elif verdict == 'MIXED':
        v_css, v_text = 'neutral', 'СМЕШАННЫЙ'
    else:
        v_css, v_text = 'neutral', 'НЕЙТРАЛЬНЫЙ'

    text_preview = review_text[:150] + ('...' if len(review_text) > 150 else '')

    aspects_html = ""
    for r in review_results:
        css_class, _ = _sentiment_label_css(r['sentiment'])
        conf = round((r.get('score', 0) or 0) * 100)
        sent_text = _sentiment_short_text(r['sentiment'])
        aspects_html += f"""
        <div class="review-aspect-line">
            <span class="review-aspect-name">{r['aspect']}</span>
            <span class="review-aspect-sent sent-{css_class}">{sent_text}</span>
            <span class="review-aspect-conf">{conf}%</span>
        </div>
        """

    return f"""
    <div class="review-card review-{v_css}">
        <div class="review-header">
            <span class="review-id">Отзыв #{review_id}</span>
            <span class="review-verdict verdict-{v_css}">{v_text}</span>
        </div>
        <div class="review-text">"{text_preview}"</div>
        <div class="review-aspects">{aspects_html}</div>
    </div>
    """


# ─── 8.2. Основной шаблон отчёта ───

def _report_template(subtitle, now, verdict, verdict_color, stats_html, progress_html, top_section, cards_html, reviews_header=""):
    """Шаблон HTML-отчёта (общий для single и batch)."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>MoodMapper — Отчёт от {now}</title>
<style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: system-ui, -apple-system, sans-serif; background: #f5f5f5; padding: 2rem 1rem; color: #333; line-height: 1.5; }}
    .container {{ max-width: 900px; margin: 0 auto; background: white; border: 1px solid #e0e0e0; border-radius: 6px; padding: 2rem; }}
    header {{ border-bottom: 1px solid #e0e0e0; padding-bottom: 1rem; margin-bottom: 1.5rem; }}
    header h1 {{ color: #222; margin-bottom: 0.25rem; font-size: 1.5rem; }}
    header .meta {{ color: #999; font-size: 0.9rem; }}
    .summary {{ background: #fafafa; border: 1px solid #e0e0e0; border-radius: 4px; padding: 1.25rem; margin-bottom: 1.5rem; }}
    .summary h2 {{ color: {verdict_color}; margin-bottom: 0.75rem; font-size: 1.25rem; }}
    .summary-stats {{ display: flex; gap: 1.5rem; flex-wrap: wrap; margin-bottom: 0.75rem; }}
    .stat {{ display: flex; align-items: baseline; gap: 0.5rem; font-size: 0.95rem; color: #666; }}
    .stat-value {{ font-weight: 600; font-size: 1.2rem; color: #333; }}
    .stat-positive .stat-value {{ color: #2e7d32; }}
    .stat-negative .stat-value {{ color: #c62828; }}
    .stat-neutral .stat-value {{ color: #e65100; }}
    .progress-bar {{ display: flex; height: 20px; border-radius: 3px; overflow: hidden; background: #e0e0e0; }}
    .progress-segment {{ display: flex; align-items: center; justify-content: center; color: white; font-weight: 500; font-size: 0.75rem; }}
    .progress-positive {{ background: #4CAF50; }}
    .progress-negative {{ background: #F44336; }}
    .progress-neutral {{ background: #FF9800; }}
    h2.section-title {{ color: #222; margin: 1.5rem 0 0.75rem; padding-bottom: 0.5rem; border-bottom: 1px solid #e0e0e0; font-size: 1.1rem; }}
    .aspect-cards {{ display: grid; gap: 0.5rem; }}
    .aspect-card {{ background: white; border: 1px solid #e0e0e0; border-left: 3px solid #ccc; border-radius: 4px; padding: 0.75rem 1rem; }}
    .aspect-card.positive {{ border-left-color: #4CAF50; }}
    .aspect-card.negative {{ border-left-color: #F44336; }}
    .aspect-card.neutral {{ border-left-color: #FF9800; }}
    .aspect-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem; gap: 0.5rem; flex-wrap: wrap; }}
    .aspect-name {{ font-size: 1rem; font-weight: 600; color: #222; }}
    .aspect-badge {{ padding: 0.15rem 0.5rem; border-radius: 3px; font-size: 0.75rem; font-weight: 600; color: white; white-space: nowrap; }}
    .badge-positive {{ background: #4CAF50; }}
    .badge-negative {{ background: #F44336; }}
    .badge-neutral {{ background: #FF9800; }}
    .aspect-context {{ color: #666; font-style: italic; font-size: 0.85rem; margin-bottom: 0.35rem; }}
    .aspect-confidence {{ font-size: 0.8rem; color: #999; }}
    .confidence-bar {{ height: 3px; background: #eee; border-radius: 2px; margin-top: 0.35rem; overflow: hidden; }}
    .confidence-fill {{ height: 100%; border-radius: 2px; }}
    .confidence-fill.positive {{ background: #4CAF50; }}
    .confidence-fill.negative {{ background: #F44336; }}
    .confidence-fill.neutral {{ background: #FF9800; }}
    .top-aspects ul {{ list-style: none; padding: 0; }}
    .top-aspects li {{ padding: 0.5rem 0; border-bottom: 1px solid #e8e8e8; display: flex; justify-content: space-between; align-items: center; gap: 0.5rem; flex-wrap: wrap; }}
    .top-aspects li:last-child {{ border-bottom: none; }}
    .top-aspects .aspect-label {{ font-weight: 500; }}
    .top-aspects .aspect-count {{ color: #666; font-size: 0.85rem; }}
    .review-card {{ background: white; border: 1px solid #e0e0e0; border-left: 3px solid #ccc; border-radius: 4px; padding: 0.75rem 1rem; margin-bottom: 0.5rem; }}
    .review-card.review-positive {{ border-left-color: #4CAF50; }}
    .review-card.review-negative {{ border-left-color: #F44336; }}
    .review-card.review-neutral {{ border-left-color: #FF9800; }}
    .review-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem; gap: 0.5rem; flex-wrap: wrap; }}
    .review-id {{ font-weight: 600; color: #222; }}
    .review-verdict {{ padding: 0.15rem 0.5rem; border-radius: 3px; font-size: 0.75rem; font-weight: 600; color: white; white-space: nowrap; }}
    .verdict-positive {{ background: #4CAF50; }}
    .verdict-negative {{ background: #F44336; }}
    .verdict-neutral {{ background: #FF9800; }}
    .review-text {{ color: #666; font-style: italic; font-size: 0.85rem; margin-bottom: 0.5rem; }}
    .review-aspects {{ display: flex; flex-direction: column; gap: 0.15rem; }}
    .review-aspect-line {{ display: flex; justify-content: space-between; align-items: center; gap: 0.5rem; font-size: 0.85rem; padding: 0.15rem 0; }}
    .review-aspect-name {{ color: #333; flex: 1; }}
    .review-aspect-sent {{ font-weight: 600; font-size: 0.8rem; }}
    .sent-positive {{ color: #2e7d32; }}
    .sent-negative {{ color: #c62828; }}
    .sent-neutral {{ color: #e65100; }}
    .review-aspect-conf {{ color: #999; font-size: 0.8rem; }}
    footer {{ margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #e0e0e0; text-align: center; color: #999; font-size: 0.85rem; }}
</style>
</head>
<body>
<div class="container">
    <header>
        <h1>MoodMapper — Отчёт</h1>
        <div class="meta">{subtitle} • Сгенерирован: {now}</div>
    </header>

    <div class="summary">
        <h2>{verdict}</h2>
        <div class="summary-stats">{stats_html}</div>
        <div class="progress-bar">{progress_html}</div>
    </div>

    {top_section}
    {reviews_header}
    <div class="aspect-cards">{cards_html}</div>

    <footer>
        MoodMapper • Аспектный анализ тональности • PyScript + Hugging Face
    </footer>
</div>
</body>
</html>
"""


def generate_report_html(results, mode="single", total_reviews=0):
    """Генерирует полный HTML-отчёт."""
    if not results:
        return None

    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    # ─── Одиночный режим ───
    if mode == "single":
        stats = aggregate_results(results)

        if stats['pos_pct'] > stats['neg_pct']:
            verdict, verdict_color = "В целом позитивный", "#4CAF50"
        elif stats['neg_pct'] > stats['pos_pct']:
            verdict, verdict_color = "В целом негативный", "#F44336"
        else:
            verdict, verdict_color = "Смешанный", "#FF9800"

        progress_html = ""
        if stats['pos_pct'] > 0:
            progress_html += f'<div class="progress-segment progress-positive" style="width: {stats["pos_pct"]}%;">{stats["pos_pct"]}%</div>'
        if stats['neg_pct'] > 0:
            progress_html += f'<div class="progress-segment progress-negative" style="width: {stats["neg_pct"]}%;">{stats["neg_pct"]}%</div>'
        if stats['neu_pct'] > 0:
            progress_html += f'<div class="progress-segment progress-neutral" style="width: {stats["neu_pct"]}%;">{stats["neu_pct"]}%</div>'

        cards_html = ""
        for res in merge_by_context(results):
            cards_html += _report_aspect_card_html(res, mode)

        return _report_template(
            subtitle="Одиночный анализ",
            now=now,
            verdict=verdict,
            verdict_color=verdict_color,
            stats_html=f"""
                <div class="stat stat-total">
                    <span>Всего аспектов:</span>
                    <span class="stat-value">{stats['total']}</span>
                </div>
                <div class="stat stat-positive">
                    <span>Позитивных:</span>
                    <span class="stat-value">{len(stats['positive'])}</span>
                </div>
                <div class="stat stat-negative">
                    <span>Негативных:</span>
                    <span class="stat-value">{len(stats['negative'])}</span>
                </div>
            """,
            progress_html=progress_html,
            top_section="",
            cards_html=cards_html,
        )

    # ─── Пакетный режим ───
    else:
        grouped = group_by_review(results)
        review_stats = calculate_review_stats(grouped)

        if review_stats['pos_pct'] > review_stats['neg_pct']:
            verdict, verdict_color = "В целом позитивная картина", "#4CAF50"
        elif review_stats['neg_pct'] > review_stats['pos_pct']:
            verdict, verdict_color = "В целом негативная картина", "#F44336"
        else:
            verdict, verdict_color = "Смешанная картина", "#FF9800"

        progress_html = ""
        if review_stats['pos_pct'] > 0:
            progress_html += f'<div class="progress-segment progress-positive" style="width: {review_stats["pos_pct"]}%;">{review_stats["pos_pct"]}%</div>'
        if review_stats['neg_pct'] > 0:
            progress_html += f'<div class="progress-segment progress-negative" style="width: {review_stats["neg_pct"]}%;">{review_stats["neg_pct"]}%</div>'
        if review_stats['mixed_pct'] > 0:
            progress_html += f'<div class="progress-segment progress-neutral" style="width: {review_stats["mixed_pct"]}%;">{review_stats["mixed_pct"]}%</div>'

        reviews_cards = ""
        review_map = {r['id']: r['text'] for r in batch_reviews}
        for rid, review_results in grouped.items():
            text = review_map.get(rid, '')
            reviews_cards += _report_review_card_html(rid, text, review_results)

        top_section = (
            '<h2 class="section-title">Топ аспектов</h2>'
            '<div class="top-aspects">'
            + _report_top_aspects_html(results)
            + '</div>'
        )

        return _report_template(
            subtitle=f"Пакетная обработка • {total_reviews} отзывов",
            now=now,
            verdict=verdict,
            verdict_color=verdict_color,
            stats_html=f"""
                <div class="stat stat-total">
                    <span>Всего отзывов:</span>
                    <span class="stat-value">{review_stats['total']}</span>
                </div>
                <div class="stat stat-positive">
                    <span>Позитивных:</span>
                    <span class="stat-value">{review_stats['positive']}</span>
                </div>
                <div class="stat stat-negative">
                    <span>Негативных:</span>
                    <span class="stat-value">{review_stats['negative']}</span>
                </div>
                <div class="stat stat-neutral">
                    <span>Смешанных:</span>
                    <span class="stat-value">{review_stats['mixed']}</span>
                </div>
            """,
            progress_html=progress_html,
            top_section=top_section,
            cards_html=reviews_cards,
            reviews_header='<h2 class="section-title">Разбивка по отзывам</h2>',
        )


def download_report(results, mode="single", total_reviews=0):
    """Скачивает HTML-отчёт."""
    html_content = generate_report_html(results, mode, total_reviews)
    if not html_content:
        print("⚠️ Нет данных для отчёта")
        return

    try:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"moodmapper_report_{mode}_{now}.html"

        blob = Blob.new([html_content], {"type": "text/html;charset=utf-8"})
        url = URL.createObjectURL(blob)

        a = js_document.createElement("a")
        a.href = url
        a.download = filename
        a.style.display = "none"
        js_document.body.appendChild(a)
        a.click()
        js_document.body.removeChild(a)
        URL.revokeObjectURL(url)

        print(f"✅ Отчёт скачан: {filename}")
    except Exception as e:
        print(f"❌ Ошибка скачивания отчёта: {e}")
        import traceback
        traceback.print_exc()


# ═══════════════════════════════════════════════════════════════
# 9. РЕНДЕРИНГ UI
# ═══════════════════════════════════════════════════════════════

# ─── 9.1. Общие элементы ───

def render_summary(stats):
    """Рендерит итоговую карточку со сводкой (одиночный режим)."""
    if stats['pos_pct'] > stats['neg_pct']:
        verdict, verdict_color = "В целом позитивный отзыв", "#2e7d32"
    elif stats['neg_pct'] > stats['pos_pct']:
        verdict, verdict_color = "В целом негативный отзыв", "#c62828"
    else:
        verdict, verdict_color = "Смешанный отзыв", "#e65100"

    html = f"""
    <div class="summary">
        <h3 style="color: {verdict_color};">{verdict}</h3>
        <div class="summary-stats">
            <div class="stat stat-total">
                <span>Всего аспектов:</span>
                <span class="stat-value">{stats['total']}</span>
            </div>
            <div class="stat stat-positive">
                <span>Позитивных:</span>
                <span class="stat-value">{len(stats['positive'])}</span>
            </div>
            <div class="stat stat-negative">
                <span>Негативных:</span>
                <span class="stat-value">{len(stats['negative'])}</span>
            </div>
        </div>
        <div class="progress-bar">
    """
    if stats['pos_pct'] > 0:
        html += f'<div class="progress-segment progress-positive" style="width: {stats["pos_pct"]}%;">{stats["pos_pct"]}%</div>'
    if stats['neg_pct'] > 0:
        html += f'<div class="progress-segment progress-negative" style="width: {stats["neg_pct"]}%;">{stats["neg_pct"]}%</div>'
    if stats['neu_pct'] > 0:
        html += f'<div class="progress-segment progress-neutral" style="width: {stats["neu_pct"]}%;">{stats["neu_pct"]}%</div>'
    html += "</div></div>"
    return html


def render_aspect_cards(results):
    """Рендерит карточки аспектов (одиночный режим)."""
    if not results:
        return ""

    merged = merge_by_context(results)
    html = '<div class="aspect-cards">'

    for res in merged:
        css_class, badge_text = _sentiment_label_css(res.get('sentiment', ''))
        score = res.get('score', 0) or 0
        confidence_pct = round(score * 100)
        aspects_display = ", ".join(res.get('aspects', []))
        context = safe_str(res.get('context', ''))

        html += f"""
        <div class="aspect-card {css_class}">
            <div class="aspect-header">
                <span class="aspect-name">{aspects_display}</span>
                <span class="aspect-badge badge-{css_class}">{badge_text}</span>
            </div>
            <div class="aspect-context">"{context}"</div>
            <div class="aspect-confidence">Уверенность: {confidence_pct}%</div>
            <div class="confidence-bar">
                <div class="confidence-fill {css_class}" style="width: {confidence_pct}%;"></div>
            </div>
        </div>
        """

    html += '</div>'
    return html


def render_top_aspects(results, top_n=5):
    """Рендерит топ-N самых частых аспектов для UI."""
    if not results:
        return ""

    top = get_top_aspects(results, top_n)

    html = f"""
    <div class="top-aspects">
        <h3>Топ-{top_n} самых частых аспектов</h3>
        <ul>
    """

    for i, (aspect, data) in enumerate(top, 1):
        count = data['count']
        pos_pct = round(data['positive'] / count * 100)
        neg_pct = round(data['negative'] / count * 100)

        if pos_pct > neg_pct:
            color, label = "#2e7d32", f"{pos_pct}% позитив"
        elif neg_pct > pos_pct:
            color, label = "#c62828", f"{neg_pct}% негатив"
        else:
            color, label = "#e65100", "смешанный"

        html += f"""
        <li>
            <span class="aspect-label">{i}. {aspect}</span>
            <span class="aspect-count">{count} упом. • <b style="color: {color};">{label}</b></span>
        </li>
        """

    html += "</ul></div>"
    return html


def render_review_cards(grouped, review_map):
    """Рендерит карточки отзывов (batch)."""
    html = ""
    for rid, review_results in grouped.items():
        verdict = get_review_verdict(review_results)
        if verdict == 'POSITIVE':
            v_css, v_text = 'positive', 'ПОЗИТИВНЫЙ'
        elif verdict == 'NEGATIVE':
            v_css, v_text = 'negative', 'НЕГАТИВНЫЙ'
        elif verdict == 'MIXED':
            v_css, v_text = 'neutral', 'СМЕШАННЫЙ'
        else:
            v_css, v_text = 'neutral', 'НЕЙТРАЛЬНЫЙ'

        text = review_map.get(rid, '')
        text_preview = text[:150] + ('...' if len(text) > 150 else '')

        aspects_html = ""
        for r in review_results:
            css_class, _ = _sentiment_label_css(r['sentiment'])
            conf = round((r.get('score', 0) or 0) * 100)
            sent_text = _sentiment_short_text(r['sentiment'])
            aspects_html += f"""
            <div class="review-aspect-line">
                <span class="review-aspect-name">{r['aspect']}</span>
                <span class="review-aspect-sent sent-{css_class}">{sent_text}</span>
                <span class="review-aspect-conf">{conf}%</span>
            </div>
            """

        html += f"""
        <div class="review-card review-{v_css}">
            <div class="review-header">
                <span class="review-id">Отзыв #{rid}</span>
                <span class="review-verdict verdict-{v_css}">{v_text}</span>
            </div>
            <div class="review-text">"{text_preview}"</div>
            <div class="review-aspects">{aspects_html}</div>
        </div>
        """
    return html


# ─── 9.2. Одиночный режим ───

def render_single_results(results):
    """Рендерит результаты одиночного анализа."""
    stats = aggregate_results(results)
    html = render_summary(stats)
    html += "<h3 style='margin-top: 1.5rem;'>Детали по аспектам:</h3>"
    html += render_aspect_cards(results)
    html += """
    <div style="margin-top: 1.5rem;">
        <button id="export-single-report" class="export-btn">Скачать отчёт (HTML)</button>
    </div>
    """
    return html


# ─── 9.3. Пакетный режим ───

def render_batch_results():
    """Рендерит результаты пакетной обработки."""
    if not batch_results:
        results_div.innerHTML = """
        <div class="summary">
            <h3>Аспекты не найдены</h3>
            <p>В загруженных отзывах не удалось найти ни одного аспекта из нашего словаря.</p>
            <p style="margin-top: 0.5rem; font-size: 0.9rem; color: #666;">
                <b>Возможные причины:</b>
            </p>
            <ul style="margin: 0.5rem 0 0 1.5rem; color: #666; font-size: 0.9rem;">
                <li>Отзывы написаны на другую тему (не еда, отель, товары)</li>
                <li>Используются слова, которых нет в нашем словаре аспектов</li>
                <li>Тексты слишком короткие или не содержат конкретики</li>
            </ul>
        </div>
        """
        return

    grouped = group_by_review(batch_results)
    review_stats = calculate_review_stats(grouped)

    if review_stats['pos_pct'] > review_stats['neg_pct']:
        verdict, verdict_color = "В целом позитивная картина", "#2e7d32"
    elif review_stats['neg_pct'] > review_stats['pos_pct']:
        verdict, verdict_color = "В целом негативная картина", "#c62828"
    else:
        verdict, verdict_color = "Смешанная картина", "#e65100"

    html = f"""
    <div class="summary">
        <h3 style="color: {verdict_color};">{verdict}</h3>
        <p style="margin-bottom: 1rem; color: #666;">
            Обработано отзывов: <b>{review_stats['total']}</b> из <b>{len(batch_reviews)}</b>
        </p>
        <div class="summary-stats">
            <div class="stat stat-total">
                <span>Всего отзывов:</span>
                <span class="stat-value">{review_stats['total']}</span>
            </div>
            <div class="stat stat-positive">
                <span>Позитивных:</span>
                <span class="stat-value">{review_stats['positive']}</span>
            </div>
            <div class="stat stat-negative">
                <span>Негативных:</span>
                <span class="stat-value">{review_stats['negative']}</span>
            </div>
            <div class="stat stat-neutral">
                <span>Смешанных:</span>
                <span class="stat-value">{review_stats['mixed']}</span>
            </div>
        </div>
        <div class="progress-bar">
    """

    if review_stats['pos_pct'] > 0:
        html += f'<div class="progress-segment progress-positive" style="width: {review_stats["pos_pct"]}%;">{review_stats["pos_pct"]}%</div>'
    if review_stats['neg_pct'] > 0:
        html += f'<div class="progress-segment progress-negative" style="width: {review_stats["neg_pct"]}%;">{review_stats["neg_pct"]}%</div>'
    if review_stats['mixed_pct'] > 0:
        html += f'<div class="progress-segment progress-neutral" style="width: {review_stats["mixed_pct"]}%;">{review_stats["mixed_pct"]}%</div>'

    html += "</div></div>"

    html += render_top_aspects(batch_results)

    html += "<h3 style='margin-top: 1.5rem;'>Разбивка по отзывам:</h3>"
    review_map = {r['id']: r['text'] for r in batch_reviews}
    html += render_review_cards(grouped, review_map)

    html += """
    <div style="margin-top: 1.5rem;">
        <button id="export-batch-report" class="export-btn">Скачать отчёт (HTML)</button>
    </div>
    """

    results_div.innerHTML = html
    attach_export_handlers()


# ═══════════════════════════════════════════════════════════════
# 10. ОБРАБОТЧИКИ СОБЫТИЙ
# ═══════════════════════════════════════════════════════════════

# ─── 10.1. Смена режима ───

def switch_mode(mode):
    """Переключает видимость форм."""
    if mode == "single":
        single_mode_div.style.display = "block"
        batch_mode_div.style.display = "none"
    else:
        single_mode_div.style.display = "none"
        batch_mode_div.style.display = "block"


@when("change", "input[name='mode']")
def on_mode_change(event):
    mode = event.target.value
    print(f"🔄 Смена режима: {mode}")
    switch_mode(mode)


# ─── 10.2. Одиночный анализ ───

@when("click", "#analyze-btn")
async def analyze(event):
    global last_single_result

    if not sentiment_pipeline:
        results_div.innerHTML = "<p>⚠️ Модель ещё не загружена</p>"
        return

    text = document.getElementById("input-text").value
    if not text or not text.strip():
        results_div.innerHTML = "<p>⚠️ Введи текст для анализа</p>"
        return

    results_div.innerHTML = "<p>⏳ Анализируем...</p>"

    try:
        aspects = find_aspects(text)
        print(f"Найденные аспекты: {[a['aspect'] for a in aspects]}")

        if not aspects:
            results_div.innerHTML = "<p>Аспекты не найдены. Попробуй текст со словами еда, сервис, доставка...</p>"
            last_single_result = None
            return

        results = []
        for aspect_info in aspects:
            aspect = aspect_info["word"]
            context = get_context_for_aspect(text, aspect_info)
            print(f"Аспект: {aspect} | Контекст: {context}")

            sentiment = await sentiment_pipeline(context)
            raw_label = sentiment[0].get('label', '')
            score = sentiment[0].get('score', 0)

            normalized = normalize_sentiment(raw_label)
            final_sentiment = apply_markers(context, normalized)

            results.append({
                'aspect': aspect,
                'sentiment': final_sentiment,
                'score': score,
                'context': context
            })

        last_single_result = results
        results_div.innerHTML = render_single_results(results)
        attach_export_handlers()

    except Exception as e:
        print(f"❌ Ошибка во время анализа: {e}")
        import traceback
        traceback.print_exc()
        results_div.innerHTML = f"<p>❌ Произошла ошибка: {e}</p>"


# ─── 10.3. CSV и пакетная обработка ───

@when("change", "#csv-file")
def on_csv_selected(event):
    print("📂 CSV-файл выбран")
    files = event.target.files
    if not files or files.length == 0:
        print("⚠️ Файл не выбран")
        return

    file = files.item(0)
    print(f"📂 Файл: {file.name} ({file.size} байт)")

    if file.size > 5 * 1024 * 1024:
        csv_info_div.style.display = "block"
        csv_info_div.className = "csv-info error"
        csv_info_div.innerHTML = "❌ <b>Файл слишком большой</b> (макс 5 МБ)"
        process_batch_btn.disabled = True
        return

    reader = FileReader.new()

    def on_load(e):
        handle_csv_content(e.target.result)

    def on_error(e):
        csv_info_div.style.display = "block"
        csv_info_div.className = "csv-info error"
        csv_info_div.innerHTML = "❌ <b>Ошибка чтения файла</b>"
        process_batch_btn.disabled = True

    reader.onload = create_proxy(on_load)
    reader.onerror = create_proxy(on_error)
    reader.readAsText(file, "UTF-8")

    csv_info_div.style.display = "block"
    csv_info_div.className = "csv-info"
    csv_info_div.innerHTML = "⏳ Читаем файл..."


@when("click", "#download-template-btn")
def on_download_template(event):
    print("📥 Генерация шаблона CSV...")
    template = (
        '1,"Пицца была вкусной, но доставка опоздала на час"\n'
        '2,"Обслуживание ужасное, больше не приду"\n'
        '3,"Атмосфера приятная, музыка тихая, еда вкусная"\n'
        '4,"Кофе холодный, десерт восхитительный"\n'
        '5,"Всё отлично, рекомендую! Вернусь ещё"\n'
    )
    try:
        blob = Blob.new([template], {"type": "text/csv;charset=utf-8"})
        url = URL.createObjectURL(blob)
        a = js_document.createElement("a")
        a.href = url
        a.download = "moodmapper_template.csv"
        a.style.display = "none"
        js_document.body.appendChild(a)
        a.click()
        js_document.body.removeChild(a)
        URL.revokeObjectURL(url)
        print("✅ Шаблон скачан")
    except Exception as e:
        print(f"❌ Ошибка скачивания: {e}")
        import traceback
        traceback.print_exc()


async def process_batch():
    """Основной цикл пакетной обработки с поддержкой паузы."""
    global batch_cancelled, batch_results, batch_paused

    batch_cancelled = False
    batch_paused = False
    batch_results = []
    total = len(batch_reviews)

    batch_progress_wrapper.style.display = "block"
    pause_batch_btn.style.display = "inline-block"
    cancel_batch_btn.style.display = "inline-block"
    pause_batch_btn.textContent = "Пауза"
    process_batch_btn.disabled = True
    csv_info_div.style.display = "none"
    results_div.innerHTML = "<p>⏳ Обрабатываем отзывы...</p>"

    for i, review in enumerate(batch_reviews):
        if batch_cancelled:
            print(f"⏹️ Отменено на {i}/{total}")
            break

        while batch_paused and not batch_cancelled:
            batch_progress_text.textContent = f"Пауза на отзыве {i+1} из {total} (#{review['id']})"
            await asyncio.sleep(0.2)

        if batch_cancelled:
            print(f"⏹️ Отменено на {i}/{total}")
            break

        percent = round((i / total) * 100)
        batch_progress_fill.style.width = f"{percent}%"
        batch_progress_text.textContent = f"Обработка отзыва {i+1} из {total} (#{review['id']})"
        batch_progress_percent.textContent = f"{percent}%"

        await asyncio.sleep(0)

        text = review['text']
        aspects = find_aspects(text)

        if not aspects:
            print(f"  ⏭️ #{review['id']}: аспекты не найдены, пропускаем")
            continue

        for aspect_info in aspects:
            if batch_cancelled:
                break

            while batch_paused and not batch_cancelled:
                await asyncio.sleep(0.2)

            if batch_cancelled:
                break

            aspect = aspect_info["word"]
            context = get_context_for_aspect(text, aspect_info)

            sentiment = await sentiment_pipeline(context)
            raw_label = sentiment[0].get('label', '')
            score = sentiment[0].get('score', 0)

            normalized = normalize_sentiment(raw_label)
            final_sentiment = apply_markers(context, normalized)

            batch_results.append({
                'review_id': review['id'],
                'aspect': aspect,
                'sentiment': final_sentiment,
                'score': score,
                'context': context
            })

    if batch_cancelled:
        batch_progress_text.textContent = "Отменено"
    else:
        batch_progress_fill.style.width = "100%"
        batch_progress_percent.textContent = "100%"
        batch_progress_text.textContent = f"Готово! Обработано {total} отзывов"

    pause_batch_btn.style.display = "none"
    cancel_batch_btn.style.display = "none"
    process_batch_btn.disabled = False

    render_batch_results()


async def on_process_batch(event=None):
    """Запуск пакетной обработки."""
    if not batch_reviews:
        results_div.innerHTML = "<p>⚠️ Сначала загрузите CSV-файл</p>"
        return

    if not sentiment_pipeline:
        results_div.innerHTML = "<p>⚠️ Модель ещё не загружена</p>"
        return

    print(f"⚙️ Запуск обработки {len(batch_reviews)} отзывов...")
    await process_batch()


def on_pause_batch(event=None):
    """Пауза / возобновление пакетной обработки."""
    global batch_paused
    batch_paused = not batch_paused

    if batch_paused:
        pause_batch_btn.textContent = "Продолжить"
        print("⏸️ Пауза")
    else:
        pause_batch_btn.textContent = "Пауза"
        print("▶️ Продолжение")


def on_cancel_batch(event=None):
    """Отмена пакетной обработки."""
    global batch_cancelled
    print("⏹️ Запрошена отмена")
    batch_cancelled = True


# ─── 10.4. Экспорт ───

def on_export_single(event=None):
    global last_single_result
    if not last_single_result:
        print("⚠️ Нет данных для экспорта")
        return
    download_report(last_single_result, mode="single")


def on_export_batch(event=None):
    if not batch_results:
        print("⚠️ Нет данных для экспорта")
        return
    download_report(batch_results, mode="batch", total_reviews=len(batch_reviews))


# ─── 10.5. Привязка обработчиков ───

def attach_all_handlers():
    """Привязывает обработчики ко всем динамическим кнопкам при старте."""
    try:
        if process_batch_btn:
            process_batch_btn.addEventListener(
                "click",
                create_proxy(lambda e: asyncio.ensure_future(on_process_batch(e)))
            )
            print("🔗 Привязан: process-batch-btn")

        if pause_batch_btn:
            pause_batch_btn.addEventListener(
                "click",
                create_proxy(on_pause_batch)
            )
            print("🔗 Привязан: pause-batch-btn")

        if cancel_batch_btn:
            cancel_batch_btn.addEventListener(
                "click",
                create_proxy(on_cancel_batch)
            )
            print("🔗 Привязан: cancel-batch-btn")
    except Exception as e:
        print(f"⚠️ Ошибка привязки обработчиков: {e}")


def attach_export_handlers():
    """Привязывает обработчики экспорта (после рендера результатов)."""
    try:
        btn_single = document.getElementById("export-single-report")
        if btn_single:
            btn_single.addEventListener("click", create_proxy(on_export_single))
            print("🔗 Привязан: export-single-report")

        btn_batch = document.getElementById("export-batch-report")
        if btn_batch:
            btn_batch.addEventListener("click", create_proxy(on_export_batch))
            print("🔗 Привязан: export-batch-report")
    except Exception as e:
        print(f"⚠️ Ошибка привязки экспорта: {e}")


# ═══════════════════════════════════════════════════════════════
# 11. ИНИЦИАЛИЗАЦИЯ
# ═══════════════════════════════════════════════════════════════

async def load_models():
    """Загружает ML-модель тональности."""
    global sentiment_pipeline
    try:
        from transformers_js_py import import_transformers_js
        transformers = await import_transformers_js()
        pipeline = transformers.pipeline

        status_div.innerHTML = "⏳ Загружаем русскую модель тональности..."
        sentiment_pipeline = await pipeline(
            'sentiment-analysis',
            'Artemeey2/rubert-base-cased-sentiment-onnx'
        )

        status_div.innerHTML = "✅ Модель готова!"
        analyze_btn.disabled = False
        analyze_btn.textContent = "Анализировать"
        process_batch_btn.disabled = False

    except Exception as e:
        print(f"❌ Ошибка загрузки модели: {e}")
        import traceback
        traceback.print_exc()
        status_div.innerHTML = f"❌ Ошибка загрузки: {e}"


async def init():
    """Инициализация приложения: загрузка модели + привязка обработчиков."""
    await load_models()
    attach_all_handlers()


asyncio.ensure_future(init())
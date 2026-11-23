# -*- coding: utf-8 -*-
"""Khung diễn đạt (paraphrase) cho benchmark Số phức v2.

Mỗi dạng có 3 danh sách khung theo mức độ thay đổi diễn đạt:
  mức 1: đổi từ ngữ, giữ nguyên trật tự câu
  mức 2: đổi trật tự (đưa câu hỏi lên trước / đảo dữ kiện cùng vai trò / gộp-tách câu)
  mức 3: đổi cấu trúc mạnh (cách gọi tên, nói bằng lời, thêm nhãn "Đề bài ... Yêu cầu ...")

Cú pháp khung:
  {0},{1},...   công thức $...$ của câu v1 (đúng thứ tự xuất hiện trong đề v1)
  [a|b|c]       chọn ngẫu nhiên một phương án (không lồng nhau)
  <TÊN>         macro (xem MAC) hoặc mảnh riêng của từng dạng (xem PIECES)
Công thức KHÔNG BAO GIỜ được viết trực tiếp trong khung; chỉ dùng {i}.
"""

MAC = {
    'CHO': '[Cho|Xét|Giả sử]',
    'CHO2': '[Cho|Xét]',
    'CHO2L': '[cho|xét]',
    'TM': '[thỏa mãn|thỏa|thoả mãn]',
    'TINH': '[Tính|Hãy tính|Tìm|Hãy tìm|Xác định|Hãy xác định]',
    'TIM': '[Tìm|Hãy tìm|Xác định|Hãy xác định]',
    'TINH0': '[Tính|Hãy tính]',
    'MD': '[môđun|mô-đun]',
    'MDC': '[Môđun|Mô-đun]',
    'HOI': '[Có bao nhiêu|Hỏi có bao nhiêu|Có tất cả bao nhiêu]',
    'HOIL': '[có bao nhiêu|hỏi có bao nhiêu|có tất cả bao nhiêu]',
    'INTRO': '[Trên tập hợp các số phức|Trên tập số phức|Trong tập số phức|Trong tập hợp số phức]',
    'ASK37': ('[Mệnh đề nào dưới đây đúng?|Khẳng định nào sau đây đúng?|Phát biểu nào dưới đây là đúng?|'
              'Trong các mệnh đề sau, mệnh đề nào đúng?|Chọn mệnh đề đúng dưới đây.|Hãy chọn khẳng định đúng.|'
              'Mệnh đề nào sau đây là mệnh đề đúng?]'),
    'ASK37L': '[mệnh đề nào dưới đây đúng?|khẳng định nào sau đây đúng?|phát biểu nào dưới đây là đúng?]',
    'ASKR': ('[Bán kính của đường tròn đó bằng bao nhiêu?|Hãy tính bán kính của đường tròn đó.|'
             'Tính bán kính của đường tròn đó.|Đường tròn đó có bán kính bằng bao nhiêu?|'
             'Hãy tìm bán kính của đường tròn đó.|Bán kính của đường tròn đó là bao nhiêu?]'),
    'ASKC': ('[Tâm của đường tròn đó có tọa độ là gì?|Tọa độ tâm của đường tròn đó là gì?|'
             'Hãy xác định tọa độ tâm của đường tròn đó.|Hãy tìm tọa độ tâm của đường tròn đó.|'
             'Tâm của đường tròn đó là điểm nào?]'),
    'SETW': '[các số phức|của các số phức|của số phức]',
}

# ---------------------------------------------------------------- D04
D04 = ([
    '<CHO> số phức {0}. <TIM> phần thực và phần ảo của số phức {1}.',
    '<CHO> {0}. <TIM> phần thực và phần ảo của {1}.',
    'Cho số phức {0}. Phần thực và phần ảo của số phức {1} [lần lượt ]là gì?',
    'Cho số phức {0}. [Hãy cho biết|Cho biết] phần thực và phần ảo của số phức {1}.',
    'Cho số phức {0}. Số phức {1} có phần thực và phần ảo [lần lượt ]là bao nhiêu?',
    '<CHO> số phức {0}. <TIM> phần thực, phần ảo của số phức {1}.',
], [
    '<TIM> phần thực và phần ảo của số phức {1}, biết [rằng ]{0}.',
    'Biết rằng {0}. [Hỏi phần thực|Phần thực] và phần ảo của số phức {1} [lần lượt ]là bao nhiêu?',
    'Với {0}, hãy xác định phần thực và phần ảo của số phức {1}.',
    'Số phức {1} có phần thực và phần ảo [lần lượt ]là bao nhiêu, nếu {0}?',
    'Phần thực và phần ảo của số phức {1} [lần lượt ]là gì, [biết rằng |với |trong đó ]{0}?',
    '[Với|Đối với] số phức {0}, số phức {1} có phần thực và phần ảo [lần lượt ]là bao nhiêu?',
], [
    'Cho {0} là một số phức. <TIM> phần thực và phần ảo của số phức liên hợp {1} của {z}.',
    'Đề bài cho {0}. Yêu cầu: tìm phần thực và phần ảo của số phức {1}.',
    'Một số phức được cho là {0}. Phần thực và phần ảo của số phức {1} [lần lượt ]bằng bao nhiêu?',
    'Gọi {1} là số phức liên hợp của {z}, với {0}. <TIM> phần thực và phần ảo của số phức liên hợp đó.',
    'Cho số phức {z} biết {0}. Hãy nêu phần thực và phần ảo của số phức liên hợp của {z}.',
    'Hãy xác định phần thực và phần ảo của số phức {1}, trong đó {0}.',
])

# ---------------------------------------------------------------- D14
D14 = ([
    '<CHO> hai số phức {0} và {1}. <TINH> <MD> của số phức {2}.',
    '<CHO> hai số phức {0} và {1}. <MDC> của số phức {2} bằng bao nhiêu?',
    '<CHO> {0} và {1}. <TINH> <MD> của {2}.',
    'Cho hai số phức {0}, {1}. <TIM> <MD> của số phức {2}.',
    'Cho hai số phức {0} và {1}. <MDC> của số phức {2} có giá trị là bao nhiêu?',
    'Cho hai số phức {0} và {1}. Số phức {2} có <MD> bằng bao nhiêu?',
], [
    '<TINH> <MD> của số phức {2}, biết {0} và {1}.',
    'Cho hai số phức {1} và {0}. <TINH> <MD> của số phức {2}.',
    '<TIM> <MD> của số phức {2}, trong đó {0} và {1}.',
    'Cho hai số phức {1} và {0}. Hỏi <MD> của số phức {2} bằng bao nhiêu?',
    '[Biết|Giả sử] {0} và {1}. <MDC> của số phức {2} là bao nhiêu?',
    '<MDC> của số phức {2} bằng bao nhiêu, với {0} và {1}?',
], [
    'Cho {0}; {1}. Số phức {2} có <MD> bằng bao nhiêu?',
    'Hai số phức {0} và {1} được cho trước. <TINH> <MD> của số phức {2}.',
    'Đề bài cho hai số phức {0} và {1}. Yêu cầu: tính <MD> của tổng hai số phức đó.',
    'Cho hai số phức {0} và {1}. Hãy tính <MD> của tổng của chúng.',
    'Giả sử {0} và {1}. Khi đó, <MD> của số phức {2} bằng bao nhiêu?',
    'Gọi {0} và {1} là hai số phức đã cho. Hãy tìm <MD> của số phức {2}.',
])

# ---------------------------------------------------------------- D28 / D32 (dùng chung, {2} = z)
MOD = ([
    '<TINH> <MD> của số phức {0} <TM> {1}.',
    '<CHO> số phức {0} <TM> {1}. <TINH> <MD> của {2}.',
    '<CHO> số phức {0} <TM> {1}. <MDC> của {2} bằng bao nhiêu?',
    '<TIM> <MD> của số phức {0} sao cho {1}.',
    '<CHO> số phức {0} <TM> {1}. <MDC> của số phức đó là bao nhiêu?',
    'Với số phức {0} <TM> {1}, <MD> của {2} [bằng bao nhiêu|là bao nhiêu]?',
    'Cho số phức {0} <TM> {1}. <MDC> của {2} [bằng bao nhiêu|có giá trị là bao nhiêu]?',
], [
    '<MDC> của số phức {0} <TM> {1} bằng bao nhiêu?',
    '<TIM> <MD> của {2}, biết {1}.',
    'Biết rằng {1}. Hỏi <MD> của số phức {0} bằng bao nhiêu?',
    'Số phức {0} <TM> {1}. <TINH> <MD> của nó.',
    '<MDC> của {2} là bao nhiêu, nếu {0} là số phức <TM> {1}?',
    '<TIM> <MD> của {2}, biết {0} là số phức <TM> {1}.',
], [
    'Cho phương trình {1} với ẩn {0} thuộc tập số phức. <TINH> <MD> của nghiệm của phương trình đó.',
    'Đề bài: số phức {0} <TM> {1}. Yêu cầu: tính <MD> của {2}.',
    'Trong tập số phức, phương trình {1} có nghiệm {0}. <MDC> của {2} là bao nhiêu?',
    'Nếu số phức {0} <TM> {1} thì <MD> của {2} bằng bao nhiêu?',
    'Cho số phức {0}, biết rằng {1}. <MDC> của {2} bằng bao nhiêu?',
    'Xét phương trình {1}, trong đó {0} là số phức cần tìm. <TINH> <MD> của {2}.',
    '<MDC> của số phức {0} <TM> điều kiện {1} là bao nhiêu?',
])

# ---------------------------------------------------------------- D37
D37 = ([
    '<CHO> số phức {0} <TM> {1}. <ASK37>',
    'Cho số phức {0} [sao cho|thỏa mãn] {1}. <ASK37>',
    'Xét số phức {0} <TM> {1}. <ASK37>',
    '<CHO> số phức {0} thỏa mãn đẳng thức {1}. <ASK37>',
    'Cho số phức {0} <TM> {1}. Trong các [mệnh đề|khẳng định] sau, [mệnh đề|khẳng định] nào đúng?',
], [
    'Với số phức {0} <TM> {1}, <ASK37L>',
    'Biết số phức {0} <TM> {1}. <ASK37>',
    'Số phức {0} <TM> {1}. <ASK37>',
    'Cho {1}, trong đó {0} là số phức. <ASK37>',
    'Giả sử {0} là số phức <TM> {1}. Trong các [mệnh đề|khẳng định] sau, [mệnh đề|khẳng định] nào đúng?',
    'Hãy chọn [mệnh đề|khẳng định] đúng, biết số phức {0} <TM> {1}.',
], [
    'Nếu số phức {0} <TM> {1} thì <ASK37L>',
    'Đề bài: số phức {0} <TM> {1}. Yêu cầu: chọn [mệnh đề|khẳng định] đúng.',
    'Cho phương trình {1} với ẩn {0} thuộc tập số phức. [Mệnh đề|Khẳng định] nào sau đây đúng đối với nghiệm {0} của phương trình?',
    'Xét phương trình {1} (ẩn {0} là số phức). <ASK37>',
    'Cho số phức {0} có tính chất {1}. <ASK37>',
    'Giả sử {1} với {0} là số phức. Hãy chọn [phát biểu|mệnh đề] đúng dưới đây.',
])

# ---------------------------------------------------------------- D38
D38 = ([
    '<HOI> số phức {0} <TM> {1}?',
    'Số các số phức {0} <TM> {1} là bao nhiêu?',
    'Phương trình {1} có bao nhiêu nghiệm phức {0}?',
    '<HOI> số phức {0} <TM> đẳng thức {1}?',
    '[Hãy tìm|Tìm] số các số phức {0} <TM> {1}.',
    '<HOI> số phức {0} sao cho {1}?',
], [
    'Đếm số lượng số phức {0} <TM> {1}.',
    'Số nghiệm phức {0} của phương trình {1} là bao nhiêu?',
    '<CHO2> {1}, trong đó {0} là số phức. Có bao nhiêu số phức {0} như vậy?',
    'Tập hợp các số phức {0} <TM> {1} có bao nhiêu phần tử?',
    'Hãy xác định số lượng số phức {0} <TM> {1}.',
    '<HOI> số phức {0} <TM> điều kiện {1}?',
], [
    'Đề bài: cho phương trình {1} ẩn {0} thuộc tập số phức. Yêu cầu: xác định số nghiệm của phương trình.',
    'Xét phương trình {1} trên tập số phức (ẩn {0}). Hỏi phương trình có bao nhiêu nghiệm?',
    'Trong tập số phức, phương trình {1} ẩn {0} có tất cả bao nhiêu nghiệm?',
    'Hãy cho biết có bao nhiêu số phức {0} <TM> điều kiện {1}.',
    'Cho phương trình {1} (ẩn số phức {0}). Số nghiệm của phương trình là bao nhiêu?',
    'Điều kiện {1} được thỏa mãn bởi bao nhiêu số phức {0}?',
])

# ---------------------------------------------------------------- nhóm đếm số phức thỏa hai điều kiện (D34, D35, D36, D39)
# <A> = điều kiện thứ nhất, <B> = điều kiện thứ hai (đều là mệnh đề đầy đủ)
COUNT2 = ([
    '<HOI> số phức {0} <TM> [đồng thời ]<A> và <B>?',
    'Số các số phức {0} <TM> [đồng thời ]<A> và <B> là bao nhiêu?',
    '<HOI> số phức {0} <TM> cả hai điều kiện <A> và <B>?',
    'Trong tập số phức, <HOIL> số phức {0} <TM> <A> và <B>?',
    'Tìm số các số phức {0} <TM> <A> và <B>.',
    '<HOI> số phức {0} sao cho <A> và <B>?',
], [
    'Trong các số phức {0} <TM> <A>, có bao nhiêu số phức mà <B>?',
    'Đếm số lượng số phức {0} <TM> [đồng thời ]<B> và <A>.',
    '<HOI> số phức {0} sao cho <B>, đồng thời <A>?',
    '[Cho|Xét] hệ điều kiện: <A>; <B>. <HOI> số phức {0} <TM> hệ điều kiện đó?',
    'Số phức {0} phải <TM> hai điều kiện: <A> và <B>. [Hỏi có|Có] bao nhiêu số phức như vậy?',
    'Hãy xác định số lượng số phức {0} sao cho <B> và <A>.',
], [
    'Điều kiện thứ nhất: <A>. Điều kiện thứ hai: <B>. <HOI> số phức {0} <TM> đồng thời hai điều kiện trên?',
    'Xét tập hợp các số phức {0} <TM> cả hai điều kiện: <A>; <B>. Tập hợp đó có bao nhiêu phần tử?',
    'Có bao nhiêu nghiệm phức {0} của hệ gồm hai điều kiện <A> và <B>?',
    '[Cho|Xét] số phức {0} <TM> <A>. Có bao nhiêu số phức như vậy mà <B>?',
    'Đề bài: số phức {0} <TM> <A> và <B>. Yêu cầu: tìm số các số phức {0} như vậy.',
    'Có tất cả bao nhiêu số phức {0} <TM> cả <A> lẫn <B>?',
])

# ---------------------------------------------------------------- nhóm phương trình bậc hai có tham số (D45, D46, D47, D48)
# <OBJ> đối tượng cần đếm, <ROOT> yêu cầu về nghiệm, <PAR> câu giới thiệu tham số
QUAD = ([
    '<INTRO>, <CHO2L> phương trình {0} (<PAR>). <HOI> <OBJ> để phương trình đó <ROOT>?',
    '<INTRO>, <CHO2L> phương trình {0}, trong đó <PAR>. <HOI> <OBJ> để phương trình <ROOT>?',
    '<CHO2> phương trình {0} (<PAR>). <INTRO>, <HOIL> <OBJ> để phương trình đó <ROOT>?',
    '<INTRO>, <CHO2L> phương trình {0} với <PAR>. <HOI> <OBJ> sao cho phương trình đã cho <ROOT>?',
], [
    'Với <PAR>, xét phương trình {0}. <HOI> <OBJ> để phương trình đó <ROOT>?',
    '<INTRO>, <CHO2L> phương trình {0} với <PAR>. Số <OBJ> để phương trình đó <ROOT> là bao nhiêu?',
    'Hãy [tìm|xác định] số <OBJ> sao cho phương trình {0} <ROOT>, biết <PAR>.',
    'Cho phương trình bậc hai {0} trên tập số phức, trong đó <PAR>. <HOI> <OBJ> để phương trình đã cho <ROOT>?',
    'Phương trình {0} (<PAR>) <ROOT> với bao nhiêu <OBJ>?',
], [
    'Đề bài: cho phương trình {0} trên tập số phức, <PAR>. Yêu cầu: đếm số <OBJ> để phương trình <ROOT>.',
    'Xét phương trình {0} với ẩn {z} thuộc tập số phức (<PAR>). Hãy cho biết có bao nhiêu <OBJ> để phương trình <ROOT>.',
    '<HOI> <OBJ> sao cho phương trình {0} (<PAR>) <ROOT>?',
    'Tìm số <OBJ> để phương trình {0} <ROOT>, với <PAR>.',
    'Cho <PAR>. <INTRO>, số <OBJ> để phương trình {0} <ROOT> là bao nhiêu?',
])
D45_EXTRA_L3 = ('<INTRO>, <CHO2L> phương trình {0} (<PAR>). <HOI> <OBJ> để phương trình đó có hai nghiệm phân biệt {3} '
                'có môđun bằng nhau?')

# ---------------------------------------------------------------- D49
D49 = ([
    'Phương trình nào [dưới đây|sau đây|trong các phương trình sau] [nhận|có] hai số phức {0} và {1} [là nghiệm|làm nghiệm]?',
    '[Hai số phức|Cặp số phức] {0} và {1} là nghiệm của phương trình nào [dưới đây|sau đây]?',
    'Trong các phương trình sau, phương trình nào có hai nghiệm là {0} và {1}?',
    'Trong các phương trình dưới đây, phương trình nào nhận cả {0} và {1} làm nghiệm?',
    'Phương trình nào sau đây có nghiệm là hai số phức {0} và {1}?',
    'Phương trình bậc hai nào dưới đây có hai nghiệm là {0} và {1}?',
    'Phương trình nào sau đây nhận {0} và {1} làm hai nghiệm?',
], [
    'Hãy chọn phương trình nhận {0} và {1} làm nghiệm.',
    'Tìm phương trình bậc hai [nhận|có] {0} và {1} làm hai nghiệm.',
    'Số phức {0} và số phức {1} cùng là nghiệm của phương trình nào [dưới đây|sau đây]?',
    'Chọn phương trình có hai nghiệm là {0} và {1}.',
    'Phương trình nhận {0} và {1} làm nghiệm là phương trình nào [dưới đây|sau đây]?',
    'Cho biết {0} và {1} là hai nghiệm của một phương trình. Phương trình đó là phương trình nào [dưới đây|sau đây]?',
    'Phương trình nào dưới đây có hai nghiệm phức là {0} và {1}?',
], [
    'Cho hai số phức {0} và {1}. Phương trình nào sau đây nhận cả hai số phức đó làm nghiệm?',
    'Xét hai số phức {0} và {1}. Hãy chọn phương trình mà hai số phức này đều là nghiệm.',
    'Đề bài: hai nghiệm cho trước là {0} và {1}. Yêu cầu: chọn phương trình tương ứng.',
    'Hai số phức {0} và {1} đều là nghiệm của một phương trình trong các phương trình sau. Đó là phương trình nào?',
    'Hãy tìm phương trình mà {0} và {1} là hai nghiệm của nó.',
    'Hai nghiệm của một phương trình là {0} và {1}. Hãy chọn phương trình đó.',
    'Đề bài: tìm phương trình có hai nghiệm {0} và {1}.',
])

# ---------------------------------------------------------------- D33
D33 = ([
    '<CHO> số phức {0} {1} <TM> {2}. <TINH0> {3}.',
    'Cho số phức {0} {1} <TM> {2}. <TINH0> giá trị của {3}.',
    '<CHO> số phức {0} {1} <TM> {2}. Giá trị của {3} bằng bao nhiêu?',
    'Cho số phức {0} {1} sao cho {2}. [Hãy tính|Tính] {3}.',
    '<CHO> số phức {0} {1} <TM> {2}. Tìm {3}.',
], [
    '<TINH0> {3}, biết số phức {0} {1} <TM> {2}.',
    'Với {0} {1}, <TM> {2}, hãy tính {3}.',
    'Biết {2}, trong đó {0} {1}. <TINH0> {3}.',
    'Số phức {0} {1} có tính chất {2}. Giá trị của {3} là bao nhiêu?',
    'Giá trị của {3} bằng bao nhiêu, biết {0} {1} <TM> {2}?',
], [
    'Xét số phức {0} với {1}. Biết rằng {2}. Khi đó, giá trị của {3} bằng bao nhiêu?',
    'Đề bài: số phức {0} {1} <TM> {2}. Yêu cầu: tính {3}.',
    'Gọi {0} {1} là số phức <TM> {2}. Hãy tính giá trị biểu thức {3}.',
    'Cho {2} với {0} {1}; hãy tìm giá trị của biểu thức {3}.',
    'Nếu số phức {0} {1} <TM> {2} thì {3} bằng bao nhiêu?',
])

# ---------------------------------------------------------------- D40
D40 = ([
    'Trên mặt phẳng tọa độ, [biết |]tập hợp điểm biểu diễn các số phức {0} <TM> {1} là một đường tròn. <ASKC>',
    'Trong mặt phẳng tọa độ, tập hợp các điểm biểu diễn của số phức {0} <TM> {1} là một đường tròn. <ASKC>',
    'Trên mặt phẳng tọa độ, tập hợp điểm biểu diễn <SETW> {0} sao cho {1} là một đường tròn. <ASKC>',
    '<CHO2> các số phức {0} <TM> {1}. Tập hợp điểm biểu diễn của chúng trên mặt phẳng tọa độ là một đường tròn. <ASKC>',
], [
    'Các số phức {0} <TM> {1} có điểm biểu diễn trên mặt phẳng tọa độ tạo thành một đường tròn. <ASKC>',
    'Tập hợp điểm biểu diễn của các số phức {0} <TM> {1} trên mặt phẳng phức là một đường tròn. <ASKC>',
    'Với số phức {0} <TM> {1}, tập hợp điểm biểu diễn của {0} trên mặt phẳng tọa độ là một đường tròn. <ASKC>',
    'Biết rằng các điểm biểu diễn số phức {0} <TM> {1} tạo thành một đường tròn trên mặt phẳng tọa độ. <ASKC>',
    '[Hãy xác định|Hãy tìm] tọa độ tâm của đường tròn là tập hợp điểm biểu diễn các số phức {0} <TM> {1} trên mặt phẳng tọa độ.',
], [
    'Đường tròn (C) là tập hợp điểm biểu diễn các số phức {0} <TM> {1}. [Tâm của (C) có tọa độ là gì?|Hãy tìm tọa độ tâm của (C).|Tọa độ tâm của (C) là gì?]',
    'Hãy tìm tọa độ tâm của đường tròn biểu diễn tập hợp các số phức {0} <TM> {1} trên mặt phẳng tọa độ.',
    'Đề bài: trên mặt phẳng tọa độ, các số phức {0} <TM> {1} có điểm biểu diễn tạo thành một đường tròn. Yêu cầu: xác định tọa độ tâm của đường tròn đó.',
    'Trên mặt phẳng tọa độ, đường tròn biểu diễn các số phức {0} <TM> {1} có tâm là điểm nào?',
    'Điều kiện {1} cho tập hợp các điểm biểu diễn số phức {0} trên mặt phẳng tọa độ là một đường tròn. <ASKC>',
])

# ---------------------------------------------------------------- D42  ({0}=z, {1}=tích, {2}=z)
D42 = ([
    '<CHO> các số phức {0} <TM> {1} là [số|một số] thuần ảo. Trên mặt phẳng tọa độ, tập hợp [tất cả ]các điểm biểu diễn các số phức {2} là một đường tròn. <ASKR>',
    '<CHO> số phức {0} sao cho {1} là số thuần ảo. Trên mặt phẳng tọa độ, tập hợp các điểm biểu diễn của {2} là một đường tròn. <ASKR>',
    'Xét các số phức {0} <TM> {1} là số thuần ảo. Tập hợp các điểm biểu diễn số phức {2} trên mặt phẳng tọa độ là một đường tròn. <ASKR>',
    '<CHO> các số phức {0} <TM> {1} là số thuần ảo. Tập hợp điểm biểu diễn các số phức {2} trên mặt phẳng tọa độ là một đường tròn. <ASKR>',
], [
    'Các số phức {0} <TM> {1} là số thuần ảo có điểm biểu diễn tạo thành một đường tròn trên mặt phẳng tọa độ. <ASKR>',
    'Xét tập hợp tất cả các số phức {0} sao cho {1} là số thuần ảo. Biết tập hợp điểm biểu diễn của chúng trên mặt phẳng tọa độ là một đường tròn. <ASKR>',
    'Với {0} là số phức sao cho {1} thuần ảo, tập hợp điểm biểu diễn số phức {2} trên mặt phẳng tọa độ là một đường tròn. <ASKR>',
    'Trên mặt phẳng tọa độ, các điểm biểu diễn số phức {2} <TM> {1} là số thuần ảo tạo thành một đường tròn. <ASKR>',
    '[Hãy tính|Tính] bán kính của đường tròn là tập hợp điểm biểu diễn các số phức {0} sao cho {1} là số thuần ảo.',
], [
    'Đường tròn (C) là tập hợp các điểm biểu diễn của số phức {0} <TM> điều kiện {1} là số thuần ảo, trên mặt phẳng tọa độ. [Bán kính của (C) bằng bao nhiêu?|Hãy tính bán kính của (C).|Tính bán kính của (C).]',
    'Đề bài: số phức {0} <TM> {1} là số thuần ảo; tập hợp điểm biểu diễn số phức {2} trên mặt phẳng tọa độ là một đường tròn. Yêu cầu: tính bán kính của đường tròn đó.',
    'Nếu {1} là số thuần ảo thì tập hợp điểm biểu diễn số phức {0} trên mặt phẳng tọa độ là một đường tròn. <ASKR>',
    'Hãy tìm bán kính của đường tròn biểu diễn tập hợp các số phức {0} <TM> {1} là số thuần ảo trên mặt phẳng tọa độ.',
    'Điều kiện {1} là số thuần ảo cho tập hợp các điểm biểu diễn số phức {2} trên mặt phẳng tọa độ là một đường tròn. <ASKR>',
])

# ---------------------------------------------------------------- D44 ({0}=z, {1}=|z|=R, {2}=Oxy, {3}=w=...)
D44 = ([
    '<CHO> số phức {0} <TM> {1}. Trên mặt phẳng tọa độ {2}, tập hợp điểm biểu diễn <SETW> {3} là một đường tròn. <ASKR>',
    '<CHO> số phức {0} <TM> {1}. Trong mặt phẳng tọa độ {2}, tập hợp các điểm biểu diễn của số phức {3} là một đường tròn. <ASKR>',
    '<CHO> số phức {0} sao cho {1}. Tập hợp điểm biểu diễn <SETW> {3} trên mặt phẳng tọa độ {2} là một đường tròn. <ASKR>',
    'Cho số phức {0} <TM> {1}. Tập hợp các điểm biểu diễn số phức {3} trên mặt phẳng tọa độ {2} là một đường tròn. <ASKR>',
], [
    'Với số phức {0} <TM> {1}, tập hợp điểm biểu diễn <SETW> {3} trên mặt phẳng tọa độ {2} là một đường tròn. <ASKR>',
    'Biết rằng {0} là số phức có {1}. Trên mặt phẳng tọa độ {2}, tập hợp điểm biểu diễn <SETW> {3} là một đường tròn. <ASKR>',
    'Số phức {0} <TM> {1}. Khi đó, trên mặt phẳng tọa độ {2}, tập hợp điểm biểu diễn <SETW> {3} là một đường tròn. <ASKR>',
    '[Hãy tính|Tính] bán kính của đường tròn là tập hợp điểm biểu diễn <SETW> {3} trên mặt phẳng tọa độ {2}, với {0} là số phức <TM> {1}.',
], [
    'Khi số phức {0} <TM> {1}, tập hợp điểm biểu diễn <SETW> {3} trên mặt phẳng tọa độ {2} là một đường tròn. <ASKR>',
    'Đề bài: số phức {0} <TM> {1}; số phức {3}. Trên mặt phẳng tọa độ {2}, tập hợp điểm biểu diễn của số phức {w} là một đường tròn. Yêu cầu: tính bán kính của đường tròn đó.',
    'Cho {0} là số phức có {1}, và đặt {3}. Trên mặt phẳng tọa độ {2}, tập hợp điểm biểu diễn của số phức {w} là một đường tròn. <ASKR>',
    'Trong mặt phẳng tọa độ {2}, đường tròn (C) là tập hợp điểm biểu diễn <SETW> {3}, với {0} là số phức <TM> {1}. [Bán kính của (C) bằng bao nhiêu?|Hãy tính bán kính của (C).|Tính bán kính của (C).]',
    'Hãy tìm bán kính của đường tròn biểu diễn tập hợp các số phức {3} trên mặt phẳng tọa độ {2}, biết số phức {0} <TM> {1}.',
])

# ---------------------------------------------------------------- D53 ({0}=z,w; {1}=|z|; {2}=|w|; {3}=biểu thức; {4}=|z-w|)
D53 = ([
    '<CHO> các số phức {0} <TM> {1} và {2}. Khi {3} đạt giá trị nhỏ nhất, [giá trị của ]{4} bằng bao nhiêu?',
    'Xét các số phức {0} <TM> {1} và {2}. Khi biểu thức {3} đạt giá trị nhỏ nhất thì {4} bằng bao nhiêu?',
    '<CHO> các số phức {0} <TM> {1} và {2}. <TINH0> {4} khi {3} đạt giá trị nhỏ nhất.',
    'Cho các số phức {0} <TM> {1} và {2}. Giá trị của {4} bằng bao nhiêu khi {3} đạt giá trị nhỏ nhất?',
    'Xét các số phức {0} <TM> {1} và {2}. Giá trị của {4} là bao nhiêu khi {3} đạt giá trị nhỏ nhất?',
], [
    '<TINH0> giá trị của {4} trong trường hợp {3} đạt giá trị nhỏ nhất, với {0} là các số phức <TM> {1} và {2}.',
    'Hai số phức {0} <TM> {2}, {1}. Khi {3} đạt giá trị nhỏ nhất, {4} bằng bao nhiêu?',
    'Xét các số phức {0} sao cho {2} và {1}. [Hãy tìm|Tìm] {4} khi {3} đạt giá trị nhỏ nhất.',
    'Cho {2} và {1}, trong đó {0} là các số phức. Khi {3} đạt giá trị nhỏ nhất, {4} bằng bao nhiêu?',
    'Với {0} là các số phức sao cho {1} và {2}, tính {4} khi {3} đạt giá trị nhỏ nhất.',
], [
    'Đề bài: hai số phức {0} <TM> {1}, {2}. Yêu cầu: khi {3} đạt giá trị nhỏ nhất, tính {4}.',
    'Cho các số phức {0} biết {2} và {1}. Giá trị của {4} bằng bao nhiêu, nếu {3} đạt giá trị nhỏ nhất?',
    'Với các số phức {0} <TM> {1} và {2}, hãy tính {4} trong trường hợp {3} đạt giá trị nhỏ nhất.',
    'Giả sử {0} là hai số phức có {1} và {2}. Khi {3} nhỏ nhất, hãy tìm {4}.',
    'Khi {3} đạt giá trị nhỏ nhất, hãy tính {4}, biết {0} là các số phức <TM> {1} và {2}.',
])

# ---------------------------------------------------------------- D50 ({0}=z, {1}=điều kiện, {2}=m,M (min,max), {3}=biểu thức, {4}=P=m+M)
D50 = ([
    '<CHO> các số phức {0} <TM> {1}. Gọi {2} lần lượt là giá trị nhỏ nhất và giá trị lớn nhất của {3}. <TINH> {4}.',
    '<CHO> các số phức {0} <TM> {1}. Gọi {2} lần lượt là giá trị nhỏ nhất, giá trị lớn nhất của {3}. Giá trị của {4} bằng bao nhiêu?',
    'Cho các số phức {0} <TM> {1}. [Ký hiệu|Kí hiệu|Đặt] {2} lần lượt là giá trị nhỏ nhất và giá trị lớn nhất của {3}. <TINH> {4}.',
    '<CHO> các số phức {0} <TM> {1}. Gọi {2} lần lượt là giá trị nhỏ nhất và giá trị lớn nhất của biểu thức {3}. <TINH0> {4}.',
], [
    'Trong các số phức {0} <TM> {1}, gọi {2} lần lượt là giá trị nhỏ nhất, giá trị lớn nhất của {3}. <TINH> {4}.',
    'Biết {1} với {0} là số phức. Gọi {2} lần lượt là giá trị nhỏ nhất và giá trị lớn nhất của biểu thức {3}. <TINH> {4}.',
    'Với các số phức {0} <TM> {1}, gọi {m} là giá trị nhỏ nhất và {M} là giá trị lớn nhất của {3}. Giá trị của {4} là bao nhiêu?',
    'Cho các số phức {0} <TM> {1}. Gọi {M} là giá trị lớn nhất và {m} là giá trị nhỏ nhất của {3}. <TINH> {4}.',
], [
    'Xét tập hợp các số phức {0} <TM> {1}. Biểu thức {3} có giá trị nhỏ nhất là {m} và giá trị lớn nhất là {M}. <TINH> {4}.',
    'Với {0} là số phức <TM> {1}, giá trị lớn nhất của {3} là {M}, giá trị nhỏ nhất là {m}. <TINH> {4}.',
    'Đề bài: các số phức {0} <TM> {1}; {m} và {M} lần lượt là giá trị nhỏ nhất và giá trị lớn nhất của {3}. Yêu cầu: tính {4}.',
    'Cho {1}, với {0} là số phức. Đặt {M} và {m} lần lượt là giá trị lớn nhất và giá trị nhỏ nhất của {3}. <TINH> {4}.',
])

# ---------------------------------------------------------------- D52 ({0}=z, {1}=điều kiện, {2}=M (max), {3}=m (min), {4}=|z|, {5}=M^2+m^2)
D52 = ([
    '<CHO> các số phức {0} <TM> {1}. Gọi {2} và {3} lần lượt là giá trị lớn nhất và giá trị nhỏ nhất của {4}. <TINH> {5}.',
    '<CHO> các số phức {0} <TM> {1}. Gọi {2} và {3} lần lượt là giá trị lớn nhất, giá trị nhỏ nhất của {4}. Giá trị của {5} bằng bao nhiêu?',
    'Cho các số phức {0} <TM> {1}. [Ký hiệu|Kí hiệu|Đặt] {2} và {3} lần lượt là giá trị lớn nhất và giá trị nhỏ nhất của {4}. <TINH> {5}.',
    '<CHO> các số phức {0} <TM> {1}. Gọi {2} và {3} lần lượt là giá trị lớn nhất và giá trị nhỏ nhất của biểu thức {4}. Giá trị của {5} là bao nhiêu?',
], [
    'Trong các số phức {0} <TM> {1}, gọi {2} và {3} lần lượt là giá trị lớn nhất và giá trị nhỏ nhất của {4}. <TINH> {5}.',
    'Biết {1} với {0} là số phức. Gọi {2} là giá trị lớn nhất và {3} là giá trị nhỏ nhất của {4}. <TINH> {5}.',
    'Với các số phức {0} <TM> {1}, gọi {3} là giá trị nhỏ nhất và {2} là giá trị lớn nhất của {4}. Giá trị của {5} là bao nhiêu?',
    'Cho các số phức {0} <TM> {1}. Gọi {3} và {2} lần lượt là giá trị nhỏ nhất và giá trị lớn nhất của {4}. <TINH> {5}.',
], [
    'Xét tập hợp các số phức {0} <TM> {1}. Biểu thức {4} có giá trị lớn nhất là {2} và giá trị nhỏ nhất là {3}. <TINH> {5}.',
    'Với {0} là số phức <TM> {1}, giá trị nhỏ nhất của {4} là {3}, giá trị lớn nhất là {2}. <TINH> {5}.',
    'Đề bài: các số phức {0} <TM> {1}; {2} và {3} lần lượt là giá trị lớn nhất và giá trị nhỏ nhất của {4}. Yêu cầu: tính {5}.',
    'Cho {1}, với {0} là số phức. Đặt {3} và {2} lần lượt là giá trị nhỏ nhất và giá trị lớn nhất của {4}. <TINH> {5}.',
])

# ---------------------------------------------------------------- D51
# {0}=S, {1}=z, {2}=w=1/(|z|-z), {3}=phần thực, {4}=z1,z2∈S, {5}=|z1-z2|=c, {6}=P=|z1-ki|^2-|z2-ki|^2
D51 = ([
    'Gọi {0} là tập hợp tất cả các số phức {1} sao cho số phức {2} có phần thực bằng {3}. Xét các số phức {4} <TM> {5}, giá trị lớn nhất của {6} bằng bao nhiêu?',
    'Gọi {0} là tập hợp tất cả các số phức {1} sao cho số phức {2} có phần thực bằng {3}. Xét các số phức {4} <TM> {5}. <TIM> giá trị lớn nhất của {6}.',
    'Gọi {0} là tập hợp tất cả các số phức {1} sao cho số phức {2} có phần thực bằng {3}. <TINH0> giá trị lớn nhất của {6}, với {4} <TM> {5}.',
    'Gọi {0} là tập hợp các số phức {1} sao cho số phức {2} có phần thực bằng {3}. Với {4} <TM> {5}, giá trị lớn nhất của {6} là bao nhiêu?',
    'Gọi {0} là tập hợp tất cả các số phức {1} sao cho số phức {2} có phần thực bằng {3}. Xét các số phức {4} <TM> {5}. Giá trị lớn nhất của {6} bằng bao nhiêu?',
], [
    '<CHO2> {0} là tập hợp các số phức {1} mà số phức {2} có phần thực là {3}. Với {4} <TM> {5}, tìm giá trị lớn nhất của biểu thức {6}.',
    'Tập hợp {0} gồm các số phức {1} sao cho số phức {2} có phần thực bằng {3}. Giả sử {4} <TM> {5}. Giá trị lớn nhất của {6} là bao nhiêu?',
    'Cho {0} là tập hợp tất cả các số phức {1} sao cho phần thực của số phức {2} bằng {3}. Xét {4} <TM> {5}. Hãy tìm giá trị lớn nhất của {6}.',
    'Xét {4} <TM> {5}, trong đó {0} là tập hợp tất cả các số phức {1} sao cho số phức {2} có phần thực bằng {3}. Giá trị lớn nhất của {6} bằng bao nhiêu?',
    'Với {0} là tập hợp tất cả các số phức {1} mà phần thực của số phức {2} bằng {3}, hãy tìm giá trị lớn nhất của {6}, trong đó {4} <TM> {5}.',
], [
    'Cho {5} với {4}, trong đó {0} là tập hợp tất cả các số phức {1} thỏa mãn: số phức {2} có phần thực bằng {3}. Tìm giá trị lớn nhất của {6}.',
    'Biết {0} là tập hợp các số phức {1} thỏa điều kiện phần thực của số phức {2} bằng {3}. Hãy tìm giá trị lớn nhất của {6} khi {4} và {5}.',
    'Đề bài: {0} là tập hợp tất cả các số phức {1} sao cho số phức {2} có phần thực bằng {3}; {4} <TM> {5}. Yêu cầu: tính giá trị lớn nhất của {6}.',
    'Với hai số phức {4} <TM> {5}, giá trị lớn nhất của {6} là bao nhiêu, biết {0} là tập hợp các số phức {1} sao cho số phức {2} có phần thực bằng {3}?',
    'Cho {0} là tập hợp các số phức {1} sao cho số phức {2} có phần thực bằng {3}. Biết {4} và {5}. Tìm giá trị lớn nhất của {6}.',
])

# ---------------------------------------------------------------- D54
# {0}=z1,z2,z3, {1}=|z1|=|z2|=2|z3|=c, {2}=hệ thức, {3}=A,B,C, {4}=z1,z2,z3, {5}=ABC
ASKS = ('[Diện tích tam giác {5} bằng bao nhiêu?|Tính diện tích tam giác {5}.|Hãy tính diện tích của tam giác {5}.|'
        'Diện tích của tam giác {5} là bao nhiêu?|Hãy xác định diện tích tam giác {5}.]')
D54 = ([
    '<CHO> các số phức {0} <TM> {1} và {2}. Gọi {3} lần lượt là các điểm biểu diễn của {4} trên mặt phẳng tọa độ. <ASKS>',
    'Cho các số phức {0} <TM> {2} và {1}. Gọi {3} lần lượt là các điểm biểu diễn của {4} trên mặt phẳng tọa độ. <ASKS>',
    '<CHO> các số phức {0} <TM> {1} và {2}. Trên mặt phẳng tọa độ, gọi {3} lần lượt là các điểm biểu diễn của {4}. <ASKS>',
    'Cho các số phức {0} <TM> {1} và {2}. Các điểm {3} lần lượt biểu diễn {4} trên mặt phẳng tọa độ. <ASKS>',
], [
    'Các số phức {0} <TM> {1}, {2}. Trên mặt phẳng tọa độ, {3} lần lượt là các điểm biểu diễn của {4}. <ASKS>',
    'Gọi {3} lần lượt là các điểm biểu diễn của các số phức {4} trên mặt phẳng tọa độ, biết {0} <TM> {2} và {1}. <ASKS>',
    'Trên mặt phẳng tọa độ, {3} lần lượt là điểm biểu diễn của các số phức {4}. Biết rằng {0} <TM> {1} và {2}. <ASKS>',
    '<CHO2> các số phức {0} với {2} và {1}. Gọi {3} lần lượt là các điểm biểu diễn của {4} trên mặt phẳng tọa độ. <ASKS>',
], [
    'Cho tam giác {5} có các đỉnh {3} lần lượt là điểm biểu diễn của {4} trên mặt phẳng tọa độ, trong đó {0} <TM> {1} và {2}. <ASKS>',
    'Đề bài: các số phức {0} <TM> {1} và {2}; {3} lần lượt là các điểm biểu diễn của {4} trên mặt phẳng tọa độ. Yêu cầu: tính diện tích tam giác {5}.',
    '<ASKS> Biết {3} lần lượt là các điểm biểu diễn của {4} trên mặt phẳng tọa độ, với {0} <TM> {1} và {2}.',
    'Xét ba số phức {0} có {1} và {2}. Trên mặt phẳng tọa độ, ba điểm {3} lần lượt biểu diễn {4}. <ASKS>',
])

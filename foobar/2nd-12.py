import string

def solution(x):
    l = [c for c in string.ascii_lowercase]
    
    dict_dec = {c:l[len(l)-1-i] for i, c in enumerate(l)}
    
    ans = ""
    for c in x:
        if c in dict_dec:
            ans += dict_dec[c]
        else:
            ans += c
    return ans

if __name__ == "__main__":
    print(solution("wrw blf hvv ozhg mrtsg'h vkrhlwv?"))
    # did you see last night's episode?

    print(solution("Yvzs! I xzm'g yvorvev Lzmxv olhg srh qly zg gsv xlolmb!!"))
    # Yeah! I can't believe Lance lost his job at the colony!!

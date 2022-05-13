def solution(l):
    
    def complete(version):
        list_written_version = [int(el) for el in version.split(".")]
        return tuple(list_written_version) + (0,)*(2-version.count(".")) + (len(list_written_version),)
    
    new_l = [(el, complete(el)) for el in l]
    return [el[0] for el in sorted(new_l, key=lambda x:x[1])]
    
    
if __name__ == "__main__":
    print(solution(["1.11", "2.0.0", "1.2", "2", "0.1", "1.2.1", "1.1.1", "2.0"]))
    # 0.1,1.1.1,1.2,1.2.1,1.11,2,2.0,2.0.0
    print(solution(["1.1.2", "1.0", "1.3.3", "1.0.12", "1.0.2"]))
    # 1.0,1.0.2,1.0.12,1.1.2,1.3.3

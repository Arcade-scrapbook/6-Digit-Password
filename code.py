def generate_passwords(start_index):
    start_time = time.time()
    total_passwords = len(CHARACTERS) ** PASSWORD_LENGTH
    passwords = itertools.product(CHARACTERS, repeat=PASSWORD_LENGTH)

    password_chunk_size = 100000
    password_chunk = []

    with tqdm(total=total_passwords, initial=start_index, dynamic_ncols=True) as pbar:
        for i, password in enumerate(passwords, start=start_index):
            password_str = "".join(password)
            password_chunk.append(password_str)

            if i % password_chunk_size == 0:
                save_password_chunk(start_index, password_chunk)
                start_index += len(password_chunk)
                password_chunk = []

                pbar.update(password_chunk_size)
                pbar.set_postfix(elapsed_time=get_elapsed_time(start_time), refresh=False)

        # Save the remaining passwords (if any)
        if password_chunk:
            save_password_chunk(start_index, password_chunk)
            pbar.update(len(password_chunk))
            pbar.set_postfix(elapsed_time=get_elapsed_time(start_time), refresh=False)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\n\nPassword generation completed in {elapsed_time:.2f} seconds!")


def save_password_chunk(start_index, password_chunk):
    try:
        with open(PASSWORDS_FILE2, "a+") as file:
            file.writelines([("i"+password)+"\n" for password in password_chunk])

        with open(PASSWORDS_FILE1, "a+") as file:
            file.writelines([(password)+"\n" for password in password_chunk])

        with open(LAST_PASSWORD_FILE, "a+") as last_pass_file:
            last_pass_file.write(str(start_index + len(password_chunk) - 1) + "\n")

    except Exception as e:
        print(f"Error saving passwords or last password index: {e}")

const PasswordInput = ({showPassword, ...props}) => {
    return (
        <div>
            <input {...props} type={showPassword ? 'text' : 'password'}/>
        </div>

    )
}


export default PasswordInput;
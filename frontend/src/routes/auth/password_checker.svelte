<script>
	export let password = '';
</script>

<section>
	<div class:active={password && /[a-z]/.test(password)}>lowercase</div>
	<div class:active={password && /[A-Z]/.test(password)}>uppercase</div>
	<div class:active={password && /[0-9]/.test(password)}>number</div>
	<div class:active={password && password.length >= 8 && password.length <= 18}>
		8 - 18 characters
	</div>
</section>

<style>
	section {
		display: flex;
		gap: var(--sp1);

		border-radius: var(--sp0);
		overflow: hidden;
	}
	div {
		font-size: x-small;
		color: var(--ac3);
	}
	.active {
		color: var(--cl5);
	}
</style>

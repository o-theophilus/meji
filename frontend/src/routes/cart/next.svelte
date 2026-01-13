<script>
	import { app } from '$lib/store.svelte.js';
	import { Button } from '$lib/button';

	let { value, label, btn_label, icon, icon2, onclick, children } = $props();
</script>

<div class="floater">
	<div class="floater_block">
		<div class="line space">
			<div class="total">{label}</div>
			<div class="cost">₦{value.toLocaleString()}</div>
		</div>

		<div class="checkout">
			<Button
				{icon}
				{icon2}
				--button-color="white"
				--button-background-color="var(--cl1)"
				{onclick}
			>
				{btn_label}
			</Button>
		</div>

		{@render children?.()}
	</div>
</div>

<style>
	.floater {
		position: sticky;
		bottom: var(--headerHeight);

		background-color: var(--bg1);
		border-top: 1px solid var(--bg2);
	}

	.floater_block {
		padding: 16px 24px;
		max-width: var(--mobileWidth);
		margin: auto;
	}

	.total {
		font-size: 0.8rem;
	}
	.cost {
		font-weight: 700;
		font-size: 1.2rem;
		color: var(--ft1);
	}

	.checkout {
		display: flex;
		justify-content: flex-end;
		margin-top: 16px;
	}
</style>

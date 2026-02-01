<script>
	import { app, module } from '$lib/store.svelte.js';

	import { Icon } from '$lib/macro';
	import Button from './nav.btn.svelte';
	import User from './nav.user.svelte';
</script>

<div class="section">
	<div class="block">
		<Button name="Home" icon="home" href="/"></Button>
		<Button name="Shop" icon="shop" href="/shop"></Button>
		<Button name="Save" icon="bookmark" href="/save" count={app.likes.length}></Button>
		<Button name="Cart" icon="cart" href="/cart" count={app.cart_items.length}></Button>
		<User />
	</div>
</div>

<style>
	.section {
		background-color: var(--bg);
		border-top: 1px solid var(--ol);
	}

	.block {
		display: flex;
		align-items: center;

		max-width: var(--mobileWidth);
		height: var(--headerHeight2);
		margin: auto;
	}
</style>

<script>
	import { module } from '$lib/store.js';

	import Body from '$lib/comp/card_body_fold.svelte';
	import HR from '$lib/comp/hr.svelte';
	import Button from '$lib/button.svelte';

	import Add_Cart from '$lib/item/add_cart.svelte';
	import Chat from './floater.chat.svelte';

	import Share from './floater__share.svelte';

	export let item;
</script>

<div class="floater">
	<HR />
	<Body>
		<div class="h space">
			<div class="h">
				<Add_Cart {item} />
				<Chat {item} />
			</div>
			<Button
				icon="share"
				on:click={() => {
					$module = {
						module: Share,
						item
					};
				}}
			/>
		</div>
	</Body>
</div>

<style>
	.floater {
		position: sticky;
		bottom: var(--headerHeight);
		background-color: var(--ac4);
	}

	@media screen and (min-width: 800px) {
		.floater {
			bottom: 0;
		}
	}
</style>

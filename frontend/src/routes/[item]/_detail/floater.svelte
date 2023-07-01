<script>
	import { module } from '$lib/store.js';

	import Body from '$lib/comp/card_body_fold.svelte';
	import HR from '$lib/comp/hr.svelte';
	import Button from '$lib/comp/button.svelte';

	import Add_Cart from '$lib/comp/item_add_cart.svelte';
	import Whatsapp from './whatsapp.svelte';

	import Share from './_share.svelte';

	export let item = {};
	item = item;
</script>

<div class="floater">
	<HR />
	<Body>
		<div class="h space">
			<div class="h">
				<Add_Cart {item} />
				<Whatsapp {item} />
			</div>
			<Button
				icon="share"
				on:click={() => {
					$module = {
						module: Share,
						data: {
							item
						}
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
		background-color: var(--foreground);
	}



	@media screen and (min-width: 800px) {
		.floater {
			bottom: 0;
		}
	}
</style>

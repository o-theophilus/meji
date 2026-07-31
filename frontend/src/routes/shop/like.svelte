<script>
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { app, page_state } from '$lib/store.svelte.js';
	import { quadInOut } from 'svelte/easing';
	import { scale } from 'svelte/transition';

	let { item, small = false } = $props();

	let like = $derived(app.likes.includes(item.key));

	const submit = async () => {
		let init = [...app.likes];
		if (app.likes.includes(item.key)) {
			app.likes = app.likes.filter((x) => x != item.key);
		} else {
			app.likes.push(item.key);
		}

		let response = await fetch(`${import.meta.env.VITE_BACKEND}/items/${item.key}/like`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			}
		});
		let result = await response.json();

		if (response.status == 200) {
			app.likes = result.likes;
			page_state.clear('save');
		} else {
			if (init.includes(item.key)) {
				app.likes.push(item.key);
			} else {
				app.likes = app.likes.filter((x) => x != item.key);
			}
		}
	};
</script>

<Button
	onclick={submit}
	--button-border-radius={small ? '40%' : ''}
	--button-width={small ? '32px' : '48px'}
	--button-height={small ? '32px' : '48px'}
	--button-background-color={small ? 'white' : ''}
	--button-background-color-hover={small ? 'hsl(0, 0%, 85%)' : ''}
	--button-outline-color={small ? 'transparent' : ''}
>
	<div class="block">
		{#key like}
			<div transition:scale={{ easing: quadInOut }}>
				<Icon
					icon="heart"
					--icon-fill={like ? 'red' : 'none'}
					--icon-stroke={like ? 'none' : 'hsl(0, 0%, 60%)'}
				/>
			</div>
		{/key}
	</div>
</Button>

<style>
	div {
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.block {
		position: relative;

		div {
			position: absolute;
		}
	}
</style>

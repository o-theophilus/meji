<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';

	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';
	import Center from '$lib/center.svelte';

	export let page_name;

	let text = '';
	let set = (url) => {
		let _s = '';
		let _t = '';
		let multiply = false;
		if (url.searchParams.has('search')) {
			_s = url.searchParams.get('search');
			_s = ` for [${_s}]`;
		}
		if (url.searchParams.has('tag')) {
			_t = url.searchParams.get('tag');
			multiply = _t.substring(_t.length - 2, _t.length) == ':x';
			if (multiply) {
				_t = _t.substring(0, _t.length - 2);
			}
			_t = _t.split(',');
			_t = ` with ${_t.length > 1 ? (multiply ? 'all' : 'any') : ''} tag${
				_t.length > 1 && multiply ? 's' : ''
			} [${_t.join(', ')}]`;
		}

		text = `${_s || _t ? 'Showing result' : ''}${_s}${_t}`;
	};

	onMount(() => {
		set($page.url);
	});
	$: set($page.url);
</script>

{#if text}
	<Center>
		<div class="filter">
			<span>
				{text}
			</span>

			<Button
				class="round"
				on:click={() => {
					set_state(page_name, 'search', '');
					set_state(page_name, 'tag', '');
				}}
			>
				<SVG type="close" size="8" />
			</Button>
		</div>
	</Center>
{/if}

<style>
	.filter {
		display: flex;
		gap: var(--sp2);
		justify-content: space-between;
		align-items: center;

		margin-top: var(--sp2);
		padding: var(--sp2);
		border-radius: var(--sp0);

		background-color: var(--cl1_t);
		color: var(--ac1);
		font-size: small;
	}
</style>

<script>
	import { onMount } from 'svelte';

	let { container = '', tag = 'h2', onclick } = $props();
	let headings = $state([]);

	function extractHeadings() {
		const root = document.querySelector(container);
		if (!root) return;

		const elements = root.querySelectorAll(tag);

		headings = Array.from(elements).map((el) => ({
			text: el.innerText,
			id: el.id
		}));
	}

	onMount(() => {
		extractHeadings();
	});
</script>

<ol>
	{#each headings as h}
		<li>
			<a href={'#' + h.id} {onclick}>{h.text}</a>
		</li>
	{/each}
</ol>

<style>
	ol {
		padding-left: 16px;
	}

	li {
		margin: 0.2rem 0;
	}

	a {
		text-decoration: none;
		color: var(--ft2);
		transition: color 0.2s ease-in-out;

		&:hover {
			color: var(--cl1);
		}
	}
</style>

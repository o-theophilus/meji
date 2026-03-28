<script>
	import { Button } from '$lib/button';
	import { Icon, Share } from '$lib/macro';
	import { module } from '$lib/store.svelte.js';

	let { post } = $props();
</script>

<Button onclick={() => module.open(Share, { ...post, entity_type: 'blog' })}>
	<Icon icon="share-2" />
	Share
</Button>

<script>
	import { Footer, Header, Nav } from '../_layout/index.js';

	let { data, children } = $props();
</script>

<Header />
{@render children()}
<Footer />

<div class="nav">
	<Nav />
</div>

<style>
	.nav {
		position: sticky;
		bottom: 0;
	}
</style>

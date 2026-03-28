<script>
	import { Footer, Header, Nav, Nav2 } from '../_layout/index.js';
	let { children } = $props();
</script>

<Header />
<Nav2 />
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

import { useState } from 'react';

function CodeBlock({ children, language = 'tsx' }: { children: string; language?: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(children);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="relative group my-4 rounded-xl overflow-hidden border border-gray-700 bg-gray-900">
      <div className="flex items-center justify-between px-4 py-2 bg-gray-800 border-b border-gray-700">
        <span className="text-xs text-gray-400 font-mono">{language}</span>
        <button
          onClick={handleCopy}
          className="text-xs text-gray-400 hover:text-white transition-colors flex items-center gap-1"
        >
          {copied ? (
            <>
              <i className="fas fa-check text-green-400"></i> Copiado
            </>
          ) : (
            <>
              <i className="fas fa-copy"></i> Copiar
            </>
          )}
        </button>
      </div>
      <pre className="p-4 overflow-x-auto text-sm">
        <code className="text-gray-300 font-mono whitespace-pre">{children}</code>
      </pre>
    </div>
  );
}

function FileTree({ files, level = 0 }: { files: FileNode[]; level?: number }) {
  return (
    <ul className={`${level > 0 ? 'ml-5 border-l border-gray-600 pl-3' : ''}`}>
      {files.map((file, i) => (
        <li key={i} className="my-1">
          <div className="flex items-center gap-2 py-1 px-2 rounded hover:bg-gray-800/50 transition-colors">
            <i className={`fas ${file.icon} ${file.color}`}></i>
            <span className={`font-mono text-sm ${file.highlight ? 'text-yellow-300 font-bold' : 'text-gray-300'}`}>
              {file.name}
            </span>
            {file.description && (
              <span className="text-xs text-gray-500 ml-2">— {file.description}</span>
            )}
          </div>
          {file.children && <FileTree files={file.children} level={level + 1} />}
        </li>
      ))}
    </ul>
  );
}

interface FileNode {
  name: string;
  icon: string;
  color: string;
  highlight?: boolean;
  description?: string;
  children?: FileNode[];
}

const projectFiles: FileNode[] = [
  {
    name: 'proyecto/',
    icon: 'fa-folder',
    color: 'text-yellow-400',
    children: [
      {
        name: 'src/',
        icon: 'fa-folder',
        color: 'text-blue-400',
        highlight: true,
        description: 'Código fuente principal',
        children: [
          { name: 'App.tsx', icon: 'fa-file-code', color: 'text-cyan-400', highlight: true, description: 'Componente raíz' },
          { name: 'main.tsx', icon: 'fa-file-code', color: 'text-cyan-400', description: 'Punto de entrada' },
          { name: 'index.css', icon: 'fa-file-code', color: 'text-pink-400', description: 'Estilos globales + Tailwind' },
        ],
      },
      { name: 'index.html', icon: 'fa-file-code', color: 'text-orange-400', highlight: true, description: 'HTML base' },
      { name: 'package.json', icon: 'fa-file-code', color: 'text-green-400', description: 'Dependencias y scripts' },
      { name: 'vite.config.js', icon: 'fa-file-code', color: 'text-purple-400', description: 'Configuración de Vite' },
      { name: 'tsconfig.json', icon: 'fa-file-code', color: 'text-blue-300', description: 'Configuración TypeScript' },
    ],
  },
];

function Section({ id, title, icon, children }: { id: string; title: string; icon: string; children: React.ReactNode }) {
  return (
    <section id={id} className="mb-16 scroll-mt-24">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-violet-500 to-indigo-600 flex items-center justify-center">
          <i className={`fas ${icon} text-white`}></i>
        </div>
        <h2 className="text-2xl md:text-3xl font-bold text-white">{title}</h2>
      </div>
      <div className="text-gray-300 leading-relaxed">{children}</div>
    </section>
  );
}

function TechCard({ name, description, icon, color }: { name: string; description: string; icon: string; color: string }) {
  return (
    <div className="bg-gray-800/50 backdrop-blur border border-gray-700 rounded-xl p-5 hover:border-gray-500 transition-all hover:scale-[1.02] hover:shadow-lg hover:shadow-violet-500/10">
      <div className={`w-12 h-12 rounded-lg ${color} flex items-center justify-center mb-3`}>
        <i className={`fab ${icon} text-white text-xl`}></i>
      </div>
      <h3 className="text-lg font-bold text-white mb-1">{name}</h3>
      <p className="text-sm text-gray-400">{description}</p>
    </div>
  );
}

function StepCard({ number, title, description }: { number: number; title: string; description: string }) {
  return (
    <div className="relative pl-12 pb-8 last:pb-0">
      <div className="absolute left-0 top-0 w-8 h-8 rounded-full bg-gradient-to-br from-violet-500 to-indigo-600 flex items-center justify-center text-white font-bold text-sm">
        {number}
      </div>
      <div className="absolute left-[15px] top-8 bottom-0 w-0.5 bg-gray-700 last:hidden"></div>
      <h4 className="text-white font-semibold text-lg mb-1">{title}</h4>
      <p className="text-gray-400 text-sm">{description}</p>
    </div>
  );
}

export default function App() {
  const [activeTab, setActiveTab] = useState('componente');

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-gray-950/80 backdrop-blur-xl border-b border-gray-800">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-violet-500 to-indigo-600 flex items-center justify-center">
              <i className="fas fa-terminal text-white text-sm"></i>
            </div>
            <span className="font-bold text-white hidden sm:block">Guía del Entorno</span>
          </div>
          <div className="flex gap-1 overflow-x-auto">
            {['inicio', 'estructura', 'tecnologias', 'ejemplos', 'flujo'].map((section) => (
              <a
                key={section}
                href={`#${section}`}
                className="px-3 py-1.5 text-xs md:text-sm text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-all capitalize whitespace-nowrap"
              >
                {section}
              </a>
            ))}
          </div>
        </div>
      </nav>

      {/* Hero */}
      <header id="inicio" className="pt-24 pb-16 px-4">
        <div className="max-w-6xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-violet-500/10 border border-violet-500/20 text-violet-300 text-sm mb-6">
            <i className="fas fa-rocket"></i>
            <span>React + Vite + Tailwind CSS</span>
          </div>
          <h1 className="text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-white via-violet-200 to-indigo-300 bg-clip-text text-transparent">
            Cómo Trabajar con el Entorno
          </h1>
          <p className="text-lg md:text-xl text-gray-400 max-w-2xl mx-auto mb-8">
            Una guía completa para entender la estructura del proyecto, las tecnologías disponibles y cómo crear aplicaciones web modernas.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <a href="#estructura" className="px-6 py-3 bg-gradient-to-r from-violet-600 to-indigo-600 rounded-xl text-white font-semibold hover:opacity-90 transition-opacity shadow-lg shadow-violet-500/25">
              <i className="fas fa-folder-tree mr-2"></i>Ver Estructura
            </a>
            <a href="#ejemplos" className="px-6 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white font-semibold hover:bg-gray-700 transition-colors">
              <i className="fas fa-code mr-2"></i>Ver Ejemplos
            </a>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 pb-20">
        {/* Estructura del Proyecto */}
        <Section id="estructura" title="Estructura del Proyecto" icon="fa-folder-tree">
          <p className="mb-6">
            El proyecto sigue una estructura estándar de <strong className="text-white">Vite + React + TypeScript</strong>. 
            Aquí puedes ver los archivos principales y su función:
          </p>
          
          <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6 mb-8">
            <FileTree files={projectFiles} />
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div className="bg-gray-800/50 border border-gray-700 rounded-xl p-5">
              <h4 className="text-white font-semibold mb-2 flex items-center gap-2">
                <i className="fas fa-star text-yellow-400"></i> src/App.tsx
              </h4>
              <p className="text-sm text-gray-400">
                Es el <strong className="text-white">componente raíz</strong> de tu aplicación. Todo lo que renderizas en pantalla 
                parte de aquí. Puedes importar otros componentes y organizar tu UI.
              </p>
            </div>
            <div className="bg-gray-800/50 border border-gray-700 rounded-xl p-5">
              <h4 className="text-white font-semibold mb-2 flex items-center gap-2">
                <i className="fas fa-star text-yellow-400"></i> src/main.tsx
              </h4>
              <p className="text-sm text-gray-400">
                Es el <strong className="text-white">punto de entrada</strong> que monta React en el DOM. 
                Generalmente no necesitas modificarlo.
              </p>
            </div>
            <div className="bg-gray-800/50 border border-gray-700 rounded-xl p-5">
              <h4 className="text-white font-semibold mb-2 flex items-center gap-2">
                <i className="fas fa-star text-yellow-400"></i> src/index.css
              </h4>
              <p className="text-sm text-gray-400">
                Contiene las <strong className="text-white">directivas de Tailwind CSS</strong> y cualquier estilo global que necesites.
              </p>
            </div>
            <div className="bg-gray-800/50 border border-gray-700 rounded-xl p-5">
              <h4 className="text-white font-semibold mb-2 flex items-center gap-2">
                <i className="fas fa-star text-yellow-400"></i> index.html
              </h4>
              <p className="text-sm text-gray-400">
                El <strong className="text-white">HTML base</strong> donde se inyecta la aplicación. Aquí puedes cambiar el título y agregar meta tags.
              </p>
            </div>
          </div>
        </Section>

        {/* Tecnologías */}
        <Section id="tecnologias" title="Tecnologías Disponibles" icon="fa-microchip">
          <p className="mb-6">
            Este entorno viene pre-configurado con las siguientes tecnologías:
          </p>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <TechCard
              name="React 18"
              description="Biblioteca para construir interfaces de usuario con componentes reutilizables"
              icon="fa-react"
              color="bg-cyan-600"
            />
            <TechCard
              name="TypeScript"
              description="JavaScript con tipos estáticos para código más seguro y mantenible"
              icon="fa-js"
              color="bg-blue-600"
            />
            <TechCard
              name="Vite"
              description="Build tool ultrarrápido con HMR instantáneo"
              icon="fa-bolt"
              color="bg-purple-600"
            />
            <TechCard
              name="Tailwind CSS"
              description="Framework CSS utility-first para estilos rápidos"
              icon="fa-css3-alt"
              color="bg-teal-600"
            />
          </div>

          <div className="bg-gradient-to-r from-violet-500/10 to-indigo-500/10 border border-violet-500/20 rounded-xl p-5">
            <h4 className="text-white font-semibold mb-2 flex items-center gap-2">
              <i className="fas fa-lightbulb text-yellow-400"></i> ¿Cómo usar Tailwind?
            </h4>
            <p className="text-sm text-gray-300 mb-3">
              Tailwind ya está configurado. Simplemente usa las clases de utilidad directamente en tu JSX:
            </p>
            <CodeBlock language="tsx">{`<div className="flex items-center gap-4 p-6 bg-white rounded-xl shadow-lg">
  <h1 className="text-2xl font-bold text-gray-900">¡Hola Mundo!</h1>
  <p className="text-gray-600">Estilizado con Tailwind</p>
</div>`}</CodeBlock>
          </div>
        </Section>

        {/* Ejemplos */}
        <Section id="ejemplos" title="Ejemplos de Código" icon="fa-code">
          <p className="mb-6">
            Aquí tienes ejemplos prácticos de cómo trabajar con este entorno:
          </p>

          {/* Tabs */}
          <div className="flex gap-1 mb-4 bg-gray-800/50 p-1 rounded-xl border border-gray-700 overflow-x-auto">
            {[
              { id: 'componente', label: 'Componente', icon: 'fa-cube' },
              { id: 'estado', label: 'Estado', icon: 'fa-database' },
              { id: 'estilos', label: 'Estilos', icon: 'fa-palette' },
              { id: 'layout', label: 'Layout', icon: 'fa-table-columns' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all whitespace-nowrap flex items-center gap-2 ${
                  activeTab === tab.id
                    ? 'bg-violet-600 text-white shadow-lg'
                    : 'text-gray-400 hover:text-white hover:bg-gray-700'
                }`}
              >
                <i className={`fas ${tab.icon}`}></i>
                {tab.label}
              </button>
            ))}
          </div>

          {/* Tab Content */}
          <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6">
            {activeTab === 'componente' && (
              <div>
                <h4 className="text-white font-semibold mb-3">Crear un componente básico</h4>
                <p className="text-sm text-gray-400 mb-4">
                  Los componentes son funciones que retornan JSX. Se escriben en archivos <code className="text-violet-300 bg-gray-800 px-1 rounded">.tsx</code>:
                </p>
                <CodeBlock language="tsx">{`// src/components/MiComponente.tsx
interface Props {
  nombre: string;
  edad?: number; // Prop opcional
}

export default function MiComponente({ nombre, edad }: Props) {
  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h2 className="text-xl font-bold">{nombre}</h2>
      {edad && <p className="text-gray-600">Edad: {edad}</p>}
    </div>
  );
}

// Uso en App.tsx:
import MiComponente from './components/MiComponente';

function App() {
  return <MiComponente nombre="María" edad={25} />;
}`}</CodeBlock>
              </div>
            )}

            {activeTab === 'estado' && (
              <div>
                <h4 className="text-white font-semibold mb-3">Manejar estado con useState</h4>
                <p className="text-sm text-gray-400 mb-4">
                  Usa el hook <code className="text-violet-300 bg-gray-800 px-1 rounded">useState</code> para manejar datos que cambian:
                </p>
                <CodeBlock language="tsx">{`import { useState } from 'react';

export default function Contador() {
  const [count, setCount] = useState(0);
  const [nombre, setNombre] = useState('');

  return (
    <div className="p-6 space-y-4">
      <div className="flex items-center gap-3">
        <button 
          onClick={() => setCount(count - 1)}
          className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
        >
          -
        </button>
        <span className="text-2xl font-bold">{count}</span>
        <button 
          onClick={() => setCount(count + 1)}
          className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
        >
          +
        </button>
      </div>
      
      <input
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
        placeholder="Tu nombre..."
        className="w-full px-4 py-2 border rounded-lg"
      />
      <p>Hola, {nombre || 'mundo'}!</p>
    </div>
  );
}`}</CodeBlock>
              </div>
            )}

            {activeTab === 'estilos' && (
              <div>
                <h4 className="text-white font-semibold mb-3">Patrones de estilos con Tailwind</h4>
                <p className="text-sm text-gray-400 mb-4">
                  Tailwind ofrece clases utilitarias para todo. Aquí los patrones más comunes:
                </p>
                <CodeBlock language="tsx">{`export default function EjemploEstilos() {
  return (
    <div>
      {/* Flexbox */}
      <div className="flex items-center justify-between gap-4">
        <span>Inicio</span>
        <span>Fin</span>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 bg-blue-100 rounded-lg">Card 1</div>
        <div className="p-4 bg-green-100 rounded-lg">Card 2</div>
        <div className="p-4 bg-purple-100 rounded-lg">Card 3</div>
      </div>

      {/* Responsive */}
      <h1 className="text-2xl md:text-4xl lg:text-6xl font-bold">
        Tamaño adaptable
      </h1>

      {/* Hover y transiciones */}
      <button className="px-6 py-3 bg-violet-600 text-white rounded-xl 
        hover:bg-violet-700 hover:scale-105 transition-all duration-200
        shadow-lg hover:shadow-xl">
        Botón animado
      </button>

      {/* Dark mode */}
      <div className="bg-white dark:bg-gray-800 text-black dark:text-white p-4 rounded-lg">
        Se adapta al tema
      </div>
    </div>
  );
}`}</CodeBlock>
              </div>
            )}

            {activeTab === 'layout' && (
              <div>
                <h4 className="text-white font-semibold mb-3">Estructura de Layout</h4>
                <p className="text-sm text-gray-400 mb-4">
                  Organiza tu aplicación con un layout responsivo:
                </p>
                <CodeBlock language="tsx">{`export default function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header fijo */}
      <header className="fixed top-0 left-0 right-0 bg-white shadow-sm z-50">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <h1 className="text-xl font-bold">Mi App</h1>
          <nav className="flex gap-4">
            <a href="#" className="text-gray-600 hover:text-black">Inicio</a>
            <a href="#" className="text-gray-600 hover:text-black">Acerca</a>
          </nav>
        </div>
      </header>

      {/* Contenido principal */}
      <main className="pt-16 max-w-6xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Sidebar */}
          <aside className="lg:col-span-1 bg-white p-6 rounded-xl shadow">
            <h2 className="font-bold mb-4">Sidebar</h2>
            <ul className="space-y-2">
              <li>Opción 1</li>
              <li>Opción 2</li>
            </ul>
          </aside>

          {/* Contenido */}
          <section className="lg:col-span-2 bg-white p-6 rounded-xl shadow">
            <h2 className="text-2xl font-bold mb-4">Contenido</h2>
            <p>Aquí va el contenido principal...</p>
          </section>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 mt-12">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <p>© 2026 Mi Aplicación</p>
        </div>
      </footer>
    </div>
  );
}`}</CodeBlock>
              </div>
            )}
          </div>
        </Section>

        {/* Flujo de Trabajo */}
        <Section id="flujo" title="Flujo de Trabajo" icon="fa-arrows-spin">
          <p className="mb-8">
            Así es como trabajas con este entorno paso a paso:
          </p>

          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-gray-800/50 border border-gray-700 rounded-xl p-6">
              <h4 className="text-white font-semibold mb-4 flex items-center gap-2">
                <i className="fas fa-list-check text-violet-400"></i> Pasos para crear tu app
              </h4>
              <StepCard
                number={1}
                title="Describe lo que quieres"
                description="Dile al asistente qué aplicación o página web quieres crear. Sé lo más específico posible."
              />
              <StepCard
                number={2}
                title="El código se genera"
                description="El asistente crea los archivos necesarios: componentes, estilos, y toda la lógica."
              />
              <StepCard
                number={3}
                title="Se construye el proyecto"
                description="Se ejecuta 'npm run build' para verificar que todo compila correctamente."
              />
              <StepCard
                number={4}
                title="Se sirve la aplicación"
                description="El archivo dist/index.html generado se sirve para que puedas ver el resultado."
              />
              <StepCard
                number={5}
                title="Itera y mejora"
                description="Pide cambios, correcciones o nuevas funcionalidades. El asistente actualiza los archivos."
              />
            </div>

            <div className="space-y-4">
              <div className="bg-gray-800/50 border border-gray-700 rounded-xl p-5">
                <h4 className="text-white font-semibold mb-3 flex items-center gap-2">
                  <i className="fas fa-check-circle text-green-400"></i> Lo que SÍ puedes hacer
                </h4>
                <ul className="space-y-2 text-sm text-gray-300">
                  <li className="flex items-start gap-2">
                    <i className="fas fa-check text-green-400 mt-1"></i>
                    <span>Crear componentes React funcionales y con clase</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <i className="fas fa-check text-green-400 mt-1"></i>
                    <span>Usar hooks (useState, useEffect, useRef, etc.)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <i className="fas fa-check text-green-400 mt-1"></i>
                    <span>Estilar con Tailwind CSS (ya configurado)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <i className="fas fa-check text-green-400 mt-1"></i>
                    <span>Instalar paquetes npm adicionales</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <i className="fas fa-check text-green-400 mt-1"></i>
                    <span>Crear múltiples archivos y carpetas</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <i className="fas fa-check text-green-400 mt-1"></i>
                    <span>Usar Font Awesome (ya incluido)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <i className="fas fa-check text-green-400 mt-1"></i>
                    <span>Generar imágenes con IA</span>
                  </li>
                </ul>
              </div>

              <div className="bg-gray-800/50 border border-gray-700 rounded-xl p-5">
                <h4 className="text-white font-semibold mb-3 flex items-center gap-2">
                  <i className="fas fa-circle-xmark text-red-400"></i> Consideraciones
                </h4>
                <ul className="space-y-2 text-sm text-gray-300">
                  <li className="flex items-start gap-2">
                    <i className="fas fa-info text-yellow-400 mt-1"></i>
                    <span>No hay backend/servidor — es una SPA estática</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <i className="fas fa-info text-yellow-400 mt-1"></i>
                    <span>Los datos persisten solo con localStorage</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <i className="fas fa-info text-yellow-400 mt-1"></i>
                    <span>Las APIs externas necesitan CORS habilitado</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <i className="fas fa-info text-yellow-400 mt-1"></i>
                    <span>Los assets van en la carpeta public/</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </Section>

        {/* Tips */}
        <section className="mb-16">
          <div className="bg-gradient-to-r from-violet-600/20 to-indigo-600/20 border border-violet-500/30 rounded-2xl p-8 text-center">
            <i className="fas fa-wand-magic-sparkles text-4xl text-violet-300 mb-4"></i>
            <h3 className="text-2xl font-bold text-white mb-3">¡Listo para crear!</h3>
            <p className="text-gray-300 max-w-xl mx-auto mb-6">
              Ahora que conoces el entorno, simplemente describe la aplicación que quieres crear 
              y el asistente se encargará de escribir todo el código, instalar dependencias y construir el proyecto.
            </p>
            <div className="flex flex-wrap justify-center gap-3">
              <span className="px-3 py-1.5 bg-gray-800 border border-gray-700 rounded-full text-sm text-gray-300">
                🎨 Landing pages
              </span>
              <span className="px-3 py-1.5 bg-gray-800 border border-gray-700 rounded-full text-sm text-gray-300">
                📊 Dashboards
              </span>
              <span className="px-3 py-1.5 bg-gray-800 border border-gray-700 rounded-full text-sm text-gray-300">
                🛒 E-commerce
              </span>
              <span className="px-3 py-1.5 bg-gray-800 border border-gray-700 rounded-full text-sm text-gray-300">
                📝 Blogs
              </span>
              <span className="px-3 py-1.5 bg-gray-800 border border-gray-700 rounded-full text-sm text-gray-300">
                🎮 Juegos
              </span>
              <span className="px-3 py-1.5 bg-gray-800 border border-gray-700 rounded-full text-sm text-gray-300">
                📱 Apps interactivas
              </span>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-8 px-4">
        <div className="max-w-6xl mx-auto text-center text-gray-500 text-sm">
          <p>Guía del Entorno de Desarrollo — React + Vite + Tailwind CSS + TypeScript</p>
        </div>
      </footer>
    </div>
  );
}
